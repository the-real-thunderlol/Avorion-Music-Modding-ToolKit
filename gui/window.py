from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox, QMenuBar
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt

from gui import styles, track_panel, detail_panel
from core import mod_memory, importer, export


def run():
    app = QApplication([])
    app.setStyleSheet(styles.GLOBAL_STYLESHEET)

    icon = QIcon("icon/icon.png")
    app.setWindowIcon(icon)

    window = QMainWindow()
    window.setWindowTitle("Avorion Music Toolkit")
    window.setWindowIcon(icon)
    window.resize(styles.WIDTH, styles.HEIGHT)
    window.setMinimumSize(styles.MIN_WIDTH, styles.MIN_HEIGHT)

    _build_menu(window)

    central = QWidget()
    outer = QVBoxLayout(central)
    outer.setContentsMargins(5, 5, 5, 5)
    outer.setSpacing(5)

    top = QWidget()
    top_layout = QHBoxLayout(top)
    top_layout.setContentsMargins(0, 0, 0, 0)
    top_layout.setSpacing(5)
    top_layout.addWidget(track_panel.build(), 1)
    top_layout.addWidget(detail_panel.build(), 2)

    outer.addWidget(top, 1)
    outer.addWidget(_build_export_bar(window))

    window.setCentralWidget(central)
    window.show()
    app.exec()


def _build_menu(window):
    bar = window.menuBar()
    file_menu = bar.addMenu("File")

    new_action = QAction("New", window)
    new_action.triggered.connect(lambda: mod_memory.reset())
    file_menu.addAction(new_action)

    open_action = QAction("Open Mod", window)
    open_action.triggered.connect(lambda: _open_mod(window))
    file_menu.addAction(open_action)

    # Credits on the right side of the menu bar
    right_bar = QMenuBar(bar)
    right_bar.setStyleSheet(
        "QMenuBar { background: transparent; border: none; padding: 0; }"
    )
    credits_action = QAction("Credits", window)
    credits_action.triggered.connect(lambda: _show_credits(window))
    right_bar.addAction(credits_action)
    bar.setCornerWidget(right_bar, Qt.TopRightCorner)


def _show_credits(window):
    text = (
        "<h3>Avorion Music Toolkit</h3>"
        "<p><b>Version:</b> 0.1</p>"
        "<p><b>Discord:</b> __thunderlol__</p>"
        "<p><b>GitHub:</b> "
        "<a href='https://github.com/the-real-thunderlol'>"
        "github.com/the-real-thunderlol</a></p>"
        "<p><b>Tool page:</b> "
        "<a href='https://github.com/the-real-thunderlol/Avorion-Music-Modding-ToolKit/upload/main'>"
        "Avorion-Music-Modding-ToolKit</a></p>"
    )
    box = QMessageBox(window)
    box.setWindowTitle("Credits")
    box.setTextFormat(Qt.RichText)
    box.setText(text)
    box.setTextInteractionFlags(Qt.TextBrowserInteraction)
    box.setStandardButtons(QMessageBox.Ok)
    box.exec()


def _open_mod(window):
    path, _ = QFileDialog.getOpenFileName(
        window, "Select modinfo.lua", "", "Lua files (modinfo.lua *.lua)"
    )
    if not path:
        return
    try:
        importer.open_mod(path)
    except Exception as e:
        QMessageBox.critical(window, "Open failed", str(e))


def _build_export_bar(window):
    bar = QWidget()
    bar.setFixedHeight(styles.EXPORT_BAR_HEIGHT)
    layout = QHBoxLayout(bar)
    layout.setContentsMargins(0, 0, styles.EXPORT_BAR_RIGHT_PAD, 0)
    layout.setSpacing(0)
    layout.addStretch(1)

    btn = styles.make_button("EXPORT MUSIC MOD")
    btn.setStyleSheet(styles.EXPORT_BUTTON_STYLE)
    btn.setFixedHeight(styles.EXPORT_BAR_HEIGHT)
    btn.clicked.connect(lambda: _do_export(window))
    layout.addWidget(btn)
    return bar


def _do_export(window):
    try:
        target = export.export_mod("exports")
        QMessageBox.information(window, "Exported", f"Mod exported to:\n{target}")
    except Exception as e:
        QMessageBox.critical(window, "Export failed", str(e))
