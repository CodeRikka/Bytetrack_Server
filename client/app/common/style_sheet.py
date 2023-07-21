# coding: utf-8
from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    DEVICE_CARD = "device_card"
    DEVICE_DIALOG = 'device_dialog'
    DEVICE_INTERFACE = "device_interface"
    LINK_CARD = "link_card"
    LOGIN_DIALOG = 'login_dialog'
    PLAYER_INTERFACE = "player_interface"
    MAIN_WINDOW = "main_window"
    HOME_INTERFACE = "home_interface"
    ICON_INTERFACE = "icon_interface"
    VIEW_INTERFACE = "view_interface"
    SETTING_INTERFACE = "setting_interface"
    GALLERY_INTERFACE = "gallery_interface"
    NAVIGATION_VIEW_INTERFACE = "navigation_view_interface"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/app/qss/{theme.value.lower()}/{self.value}.qss"
