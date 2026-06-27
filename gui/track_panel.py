from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QListWidgetItem, QFileDialog, QMenu, QAbstractItemView
)
from PySide6.QtCore import Qt

from gui import styles
from core import mod_memory, id_generator, name_sanitizer


_list_widget = None


def build():
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(5, 5, 5, 5)
    layout.setSpacing(5)

    # Row 1: MOD SETTINGS tile
    settings_btn = styles.make_button("MOD SETTINGS")
    settings_btn.setStyleSheet(styles.MOD_SETTINGS_TILE_STYLE)
    settings_btn.clicked.connect(_select_mod_settings)
    layout.addWidget(settings_btn)

    # Row 2: 3-column bar [Delete] [spacer] [+]
    bar = QWidget()
    bar_layout = QHBoxLayout(bar)
    bar_layout.setContentsMargins(0, 0, 0, 0)

    delete_btn = styles.make_button("Remove selected Music")
    delete_btn.setStyleSheet(styles.REMOVE_BUTTON_STYLE)
    delete_btn.clicked.connect(_delete_selected)
    bar_layout.addWidget(delete_btn, 1)

    spacer = QWidget()
    bar_layout.addWidget(spacer, 1)

    add_btn = styles.make_button("[Add Music]")
    add_btn.clicked.connect(_add_tracks)
    bar_layout.addWidget(add_btn, 1)

    layout.addWidget(bar)

    # Row 3+: track list (scrollable)
    global _list_widget
    _list_widget = QListWidget()
    _list_widget.setDragDropMode(QAbstractItemView.InternalMove)
    _list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
    _list_widget.customContextMenuRequested.connect(_show_context_menu)
    _list_widget.currentRowChanged.connect(_on_select)
    _list_widget.model().rowsMoved.connect(_on_rows_moved)
    layout.addWidget(_list_widget, 1)

    mod_memory.subscribe(_refresh)
    _refresh()
    return container


def update_track_label(tid, new_name):
    if _list_widget is None:
        return
    for i in range(_list_widget.count()):
        item = _list_widget.item(i)
        if item.data(Qt.UserRole) == tid:
            item.setText(new_name)
            break


def _select_mod_settings():
    if _list_widget is not None:
        _list_widget.blockSignals(True)
        _list_widget.setCurrentRow(-1)
        _list_widget.blockSignals(False)
    mod_memory.select("mod_settings")


def _add_tracks():
    paths, _ = QFileDialog.getOpenFileNames(
        None, "Select music files", "",
        "Audio files (*.wav *.mp3 *.flac *.ogg)"
    )
    if not paths:
        return
    for p in paths:
        name = name_sanitizer.sanitize(Path(p).stem)
        mod_memory.tracks.append({
            "id": id_generator.new_id(),
            "source_path": p,
            "display_name": name,
            "collections": set(),
        })
    mod_memory.notify()


def _delete_selected():
    sel = mod_memory.selected
    if not isinstance(sel, str) or sel == "mod_settings":
        return
    mod_memory.tracks = [t for t in mod_memory.tracks if t["id"] != sel]
    mod_memory.selected = "mod_settings"
    mod_memory.notify()


def _show_context_menu(pos):
    if _list_widget is None:
        return
    item = _list_widget.itemAt(pos)
    if item is None:
        return
    _list_widget.setCurrentItem(item)
    menu = QMenu()
    delete_action = menu.addAction("Delete")
    chosen = menu.exec(_list_widget.viewport().mapToGlobal(pos))
    if chosen == delete_action:
        _delete_selected()


def _on_select(row):
    if _list_widget is None:
        return
    if row < 0 or row >= len(mod_memory.tracks):
        return
    item = _list_widget.item(row)
    if item is None:
        return
    tid = item.data(Qt.UserRole)
    mod_memory.select(tid)


def _on_rows_moved(*args):
    if _list_widget is None:
        return
    new_order = []
    for i in range(_list_widget.count()):
        item = _list_widget.item(i)
        tid = item.data(Qt.UserRole)
        track = next((t for t in mod_memory.tracks if t["id"] == tid), None)
        if track is not None:
            new_order.append(track)
    mod_memory.tracks = new_order


def _refresh():
    if _list_widget is None:
        return
    _list_widget.blockSignals(True)
    _list_widget.clear()
    for t in mod_memory.tracks:
        item = QListWidgetItem(t["display_name"])
        item.setData(Qt.UserRole, t["id"])
        _list_widget.addItem(item)
    sel = mod_memory.selected
    if isinstance(sel, str) and sel != "mod_settings":
        for i in range(_list_widget.count()):
            if _list_widget.item(i).data(Qt.UserRole) == sel:
                _list_widget.setCurrentRow(i)
                break
    else:
        _list_widget.setCurrentRow(-1)
    _list_widget.blockSignals(False)
