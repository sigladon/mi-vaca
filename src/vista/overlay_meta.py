from src.vista.overlay import Overlay
from src.vista.ui.overlay_meta_ui import Ui_OverlayMeta


class OverlayMeta(Overlay):
    def __init__(self, parent=None):
        super().__init__(Ui_OverlayMeta(),parent)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)