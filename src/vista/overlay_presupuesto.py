from src.vista.overlay import Overlay
from src.vista.ui.overlay_presupuesto_ui import Ui_OverlayPresupuesto


class OverlayPresupuesto(Overlay):
    def __init__(self, parent=None):
        super().__init__(Ui_OverlayPresupuesto(),parent)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)