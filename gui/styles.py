### size
WIDTH      = 1280
HEIGHT     = 720
MIN_WIDTH  = 1280
MIN_HEIGHT = 720

### obsidian palette
Background_Color  = "#1e1e1e"
SideBar_Color     = "#262626"
Panel_Color       = "#2a2a2a"
Hover_Color       = "#3a3a3a"
Accent_Color      = "#4a90d9"
Text_Color        = "#e0e0e0"
Subtle_Text_Color = "#a0a0a0"
Border_Color      = "#404040"
NavBar_Color      = "#161616"

### export bar
Export_BG_Color = "#f5c518"
Export_FG_Color = "#000000"
EXPORT_BAR_HEIGHT = 40
EXPORT_BAR_RIGHT_PAD = 15

### list heading
LIST_HEADING_TEXT  = "Music"
LIST_HEADING_COLOR = "#ffffff"
LIST_HEADING_SIZE  = 16


### widget-specific stylesheets

MOD_SETTINGS_TILE_STYLE = f"""
QPushButton {{
    background-color: {Panel_Color};
    color: {Text_Color};
    font-weight: bold;
    padding: 10px;
    border: 1px solid {Border_Color};
    border-radius: 6px;
}}
QPushButton:hover {{
    background-color: {Hover_Color};
}}
"""

REMOVE_BUTTON_STYLE = """
QPushButton {
    background-color: #c0392b;
    color: #ffffff;
    border: 1px solid #8a261c;
    border-radius: 6px;
    padding: 4px 8px;
}
QPushButton:hover {
    background-color: #d64841;
}
"""

EXPORT_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {Export_BG_Color};
    color: {Export_FG_Color};
    font-weight: bold;
    padding: 0px 20px;
    border: none;
    border-radius: 6px;
}}
QPushButton:hover {{
    background-color: #ffd84d;
}}
"""

THUMB_LABEL_STYLE = f"""
background-color: {Panel_Color};
border: 1px solid {Border_Color};
border-radius: 6px;
color: {Subtle_Text_Color};
"""

TYPE_LABEL_STYLE = f"""
background-color: {Panel_Color};
padding: 4px;
border: 1px solid {Border_Color};
border-radius: 6px;
"""

DEP_PLACEHOLDER_STYLE = f"""
background-color: {Panel_Color};
color: {Subtle_Text_Color};
border: 1px dashed {Border_Color};
border-radius: 6px;
padding: 8px;
"""

H2_LABEL_STYLE = f"""
font-size: 16px;
font-weight: bold;
color: {Text_Color};
"""

FIELD_LABEL_STYLE = f"""
color: {Subtle_Text_Color};
font-size: 13px;
"""


def make_button(text=""):
    from PySide6.QtWidgets import QPushButton
    from PySide6.QtCore import Qt
    btn = QPushButton(text)
    btn.setCursor(Qt.PointingHandCursor)
    return btn


GLOBAL_STYLESHEET = f"""
QWidget {{
    background-color: {Background_Color};
    color: {Text_Color};
    font-family: Segoe UI, sans-serif;
    font-size: 13px;
}}
QListWidget, QLineEdit, QTextEdit {{
    background-color: {SideBar_Color};
    border: 1px solid {Border_Color};
    border-radius: 6px;
    selection-background-color: {Accent_Color};
    color: {Text_Color};
    padding: 3px;
}}
QPushButton {{
    background-color: {Panel_Color};
    color: {Text_Color};
    border: 1px solid {Border_Color};
    border-radius: 6px;
    padding: 4px 8px;
}}
QPushButton:hover {{
    background-color: {Hover_Color};
}}
QMenuBar {{
    background-color: {NavBar_Color};
    color: {Text_Color};
    font-size: 14px;
    padding: 4px 8px;
    border-bottom: 1px solid {Border_Color};
}}
QMenuBar::item {{
    background: transparent;
    padding: 6px 14px;
    border-radius: 4px;
}}
QMenu {{
    background-color: {NavBar_Color};
    color: {Text_Color};
    border: 1px solid {Border_Color};
    padding: 4px;
    font-size: 13px;
}}
QMenu::item {{
    padding: 6px 18px;
    border-radius: 4px;
}}
QMenuBar::item:selected, QMenu::item:selected {{
    background-color: {Hover_Color};
}}
QLabel {{
    color: {Text_Color};
    background: transparent;
}}
QCheckBox {{
    color: {Text_Color};
    background: transparent;
    font-size: 14px;
    spacing: 8px;
    padding: 3px 0;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1px solid {Border_Color};
    border-radius: 4px;
    background-color: {SideBar_Color};
}}
QCheckBox::indicator:hover {{
    border: 1px solid {Accent_Color};
}}
QCheckBox::indicator:checked {{
    background-color: {Accent_Color};
    border: 1px solid {Accent_Color};
}}
QCheckBox::indicator:disabled {{
    background-color: {Panel_Color};
    border: 1px solid {Border_Color};
}}
QScrollArea {{
    border: none;
}}
QScrollBar:vertical {{
    background: {Background_Color};
    width: 10px;
}}
QScrollBar::handle:vertical {{
    background: {Hover_Color};
    border-radius: 3px;
}}
"""
