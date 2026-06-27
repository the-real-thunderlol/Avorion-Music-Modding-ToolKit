from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QCheckBox, QFileDialog, QScrollArea
)
from PySide6.QtCore import Qt, QObject, QEvent, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPixmap

from gui import styles, track_panel
from core import mod_memory, music_lua, name_sanitizer


_scroll_area = None
_inner = None
_last_sel = object()
_last_token = -1
_thumb_label = None
_wheel_filter = None


class _SmoothWheelFilter(QObject):
    def __init__(self, scrollbar):
        super().__init__()
        self._sb = scrollbar
        self._anim = QPropertyAnimation(scrollbar, b"value")
        self._anim.setDuration(220)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            delta = event.angleDelta().y()
            if delta == 0:
                return False
            self._anim.stop()
            start = self._sb.value()
            target = max(self._sb.minimum(), min(self._sb.maximum(), start - delta))
            self._anim.setStartValue(start)
            self._anim.setEndValue(target)
            self._anim.start()
            return True
        return False


def build():
    global _scroll_area, _inner
    global _wheel_filter
    _scroll_area = QScrollArea()
    _scroll_area.setWidgetResizable(True)

    _inner = QWidget()
    QVBoxLayout(_inner)  # placeholder layout
    _scroll_area.setWidget(_inner)

    _wheel_filter = _SmoothWheelFilter(_scroll_area.verticalScrollBar())
    _scroll_area.viewport().installEventFilter(_wheel_filter)

    mod_memory.subscribe(_maybe_refresh)
    _force_refresh()
    return _scroll_area


def _maybe_refresh():
    global _last_sel, _last_token
    sel = mod_memory.selected
    token = mod_memory._full_token

    # Validate: if selected track no longer exists, fall back to mod_settings
    if isinstance(sel, str) and sel != "mod_settings":
        if not any(t["id"] == sel for t in mod_memory.tracks):
            mod_memory.selected = "mod_settings"
            sel = "mod_settings"

    if sel == _last_sel and token == _last_token:
        return
    _last_sel = sel
    _last_token = token
    _force_refresh()


def _force_refresh():
    if _inner is None:
        return
    _clear_layout(_inner.layout())

    layout = _inner.layout()
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(8)

    sel = mod_memory.selected
    if sel == "mod_settings" or sel is None:
        _build_mod_settings(layout)
    else:
        track = next((t for t in mod_memory.tracks if t["id"] == sel), None)
        if track is None:
            _build_mod_settings(layout)
        else:
            _build_track_view(layout, track)


def _clear_layout(layout):
    if layout is None:
        return
    while layout.count():
        item = layout.takeAt(0)
        w = item.widget()
        if w is not None:
            w.setParent(None)
            w.deleteLater()
        else:
            sub = item.layout()
            if sub is not None:
                _clear_layout(sub)


# --------- MOD SETTINGS ---------

def _build_mod_settings(layout):
    global _thumb_label

    layout.addWidget(_h2("MOD SETTINGS"))

    _thumb_label = QLabel()
    _thumb_label.setFixedSize(300, 300)
    _thumb_label.setAlignment(Qt.AlignCenter)
    _thumb_label.setScaledContents(False)
    _thumb_label.setStyleSheet(styles.THUMB_LABEL_STYLE)
    _update_thumb()

    thumb_wrap = QWidget()
    wrap_layout = QHBoxLayout(thumb_wrap)
    wrap_layout.setContentsMargins(0, 0, 0, 0)
    wrap_layout.addStretch(1)
    wrap_layout.addWidget(_thumb_label)
    wrap_layout.addStretch(1)
    layout.addWidget(thumb_wrap)

    thumb_btn = styles.make_button("Select Thumbnail")
    thumb_btn.clicked.connect(_pick_thumbnail)
    layout.addWidget(thumb_btn)

    layout.addWidget(_label("Name"))
    name_edit = QLineEdit(mod_memory.modinfo.get("name", ""))
    name_edit.textChanged.connect(lambda v: _set_field("name", v))
    layout.addWidget(name_edit)

    layout.addWidget(_label("Title"))
    title_edit = QLineEdit(mod_memory.modinfo.get("title", ""))
    title_edit.textChanged.connect(lambda v: _set_field("title", v))
    layout.addWidget(title_edit)

    layout.addWidget(_label("Type"))
    type_lbl = QLabel("mod")
    type_lbl.setStyleSheet(styles.TYPE_LABEL_STYLE)
    layout.addWidget(type_lbl)

    layout.addWidget(_label("Description"))
    desc_edit = QTextEdit()
    desc_edit.setPlainText(mod_memory.modinfo.get("description", ""))
    desc_edit.setFixedHeight(80)
    desc_edit.textChanged.connect(
        lambda: _set_field("description", desc_edit.toPlainText())
    )
    layout.addWidget(desc_edit)

    layout.addWidget(_label("Authors"))
    authors_container = QWidget()
    authors_layout = QVBoxLayout(authors_container)
    authors_layout.setContentsMargins(0, 0, 0, 0)
    authors_layout.setSpacing(4)
    _build_authors_rows(authors_layout)
    layout.addWidget(authors_container)

    layout.addWidget(_label("Version"))
    ver_edit = QLineEdit(mod_memory.modinfo.get("version", "1.0"))
    ver_edit.textChanged.connect(lambda v: _set_field("version", v))
    layout.addWidget(ver_edit)

    layout.addWidget(_label("Dependencies"))
    dep_lbl = QLabel("[NOT PROGRAMMED YET]")
    dep_lbl.setAlignment(Qt.AlignCenter)
    dep_lbl.setStyleSheet(styles.DEP_PLACEHOLDER_STYLE)
    layout.addWidget(dep_lbl)

    server_cb = QCheckBox("serverSideOnly")
    server_cb.setChecked(mod_memory.modinfo.get("serverSideOnly", False))
    server_cb.toggled.connect(lambda v: _set_field("serverSideOnly", v))
    layout.addWidget(server_cb)

    client_cb = QCheckBox("clientSideOnly")
    client_cb.setChecked(mod_memory.modinfo.get("clientSideOnly", False))
    client_cb.toggled.connect(lambda v: _set_field("clientSideOnly", v))
    layout.addWidget(client_cb)

    save_cb = QCheckBox("saveGameAltering")
    save_cb.setChecked(mod_memory.modinfo.get("saveGameAltering", False))
    save_cb.setEnabled(False)
    layout.addWidget(save_cb)

    layout.addWidget(_label("Contact"))
    contact_edit = QLineEdit(mod_memory.modinfo.get("contact", ""))
    contact_edit.textChanged.connect(lambda v: _set_field("contact", v))
    layout.addWidget(contact_edit)

    layout.addStretch(1)


def _build_authors_rows(layout):
    while layout.count():
        item = layout.takeAt(0)
        w = item.widget()
        if w is not None:
            w.setParent(None)
            w.deleteLater()

    authors = mod_memory.modinfo.setdefault("authors", [""])
    if not authors:
        authors.append("")

    for idx in range(len(authors)):
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)

        edit = QLineEdit(authors[idx])
        edit.textChanged.connect(lambda v, i=idx: _set_author(i, v))
        row_layout.addWidget(edit, 1)

        plus = styles.make_button("+")
        plus.setFixedWidth(30)
        plus.clicked.connect(lambda _=False, i=idx: _add_author(i + 1, layout))
        row_layout.addWidget(plus)

        minus = styles.make_button("-")
        minus.setFixedWidth(30)
        minus.setEnabled(len(authors) > 1)
        minus.clicked.connect(lambda _=False, i=idx: _remove_author(i, layout))
        row_layout.addWidget(minus)

        layout.addWidget(row)


def _set_field(field, value):
    mod_memory.modinfo[field] = value


def _set_author(idx, value):
    authors = mod_memory.modinfo.get("authors", [])
    if 0 <= idx < len(authors):
        authors[idx] = value


def _add_author(at, layout):
    mod_memory.modinfo.setdefault("authors", [""]).insert(at, "")
    _build_authors_rows(layout)


def _remove_author(idx, layout):
    authors = mod_memory.modinfo.get("authors", [])
    if len(authors) <= 1:
        return
    authors.pop(idx)
    _build_authors_rows(layout)


def _pick_thumbnail():
    path, _ = QFileDialog.getOpenFileName(
        None, "Select thumbnail", "",
        "Images (*.jpg *.jpeg *.png)"
    )
    if not path:
        return
    mod_memory.thumbnail_path = path
    _update_thumb()


def _update_thumb():
    if _thumb_label is None:
        return
    if mod_memory.thumbnail_path:
        pix = QPixmap(mod_memory.thumbnail_path)
        if not pix.isNull():
            pix = pix.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        _thumb_label.setPixmap(pix)
        _thumb_label.setText("")
        return
    _thumb_label.setPixmap(QPixmap())
    _thumb_label.setText("No thumbnail")


# --------- TRACK VIEW ---------

def _build_track_view(layout, track):
    layout.addWidget(_h2(f"Track: {track['display_name']}"))

    layout.addWidget(_label("Name"))
    name_edit = QLineEdit(track["display_name"])

    def on_name_changed(v):
        sanitized = name_sanitizer.sanitize(v)
        if sanitized != v:
            cursor = name_edit.cursorPosition()
            name_edit.blockSignals(True)
            name_edit.setText(sanitized)
            name_edit.setCursorPosition(min(cursor, len(sanitized)))
            name_edit.blockSignals(False)
        for t in mod_memory.tracks:
            if t["id"] == track["id"]:
                t["display_name"] = sanitized
                break
        track_panel.update_track_label(track["id"], sanitized)

    name_edit.textChanged.connect(on_name_changed)
    layout.addWidget(name_edit)

    layout.addWidget(_label("Collections"))
    for col in music_lua.COLLECTIONS:
        cb = QCheckBox(f"TrackCollection.{col}()")
        cb.setChecked(col in track["collections"])
        cb.toggled.connect(lambda v, c=col, tid=track["id"]: _toggle_collection(tid, c, v))
        layout.addWidget(cb)

    layout.addStretch(1)


def _toggle_collection(tid, col, value):
    for t in mod_memory.tracks:
        if t["id"] == tid:
            if value:
                t["collections"].add(col)
            else:
                t["collections"].discard(col)
            break


# --------- HELPERS ---------

def _h2(text):
    lbl = QLabel(text)
    lbl.setStyleSheet(styles.H2_LABEL_STYLE)
    return lbl


def _label(text):
    lbl = QLabel(text)
    lbl.setStyleSheet(styles.FIELD_LABEL_STYLE)
    return lbl
