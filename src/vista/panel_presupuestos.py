from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QMessageBox

from src.vista.overlay_presupuesto import OverlayPresupuesto
from src.vista.ui.overlay_presupuesto_ui import Ui_OverlayPresupuesto
from src.vista.ui.panel_presupuestos_ui import Ui_PanelPresupuestos


class PanelPresupuesto(QWidget):
    solicitar_mostrar_login = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.overlay: OverlayPresupuesto | None = None
        self.ui = Ui_PanelPresupuestos()
        self.ui.setupUi(self)

    def mostrar_modal(self, editando: bool = False):
        if editando:
            self.overlay.ui.btn_borrar_presupuesto.show()
        else:
            self.overlay.ui.btn_borrar_presupuesto.hide()

        if self.overlay:
            self.overlay.show()

    def ocultar_modal(self, preguntar: bool = True):
        print(str(preguntar))

        if preguntar:
            respuesta = QMessageBox.question(
                self,
                "Confirmar salida",
                f"¿Estás seguro de querer salir? Los cambios no se guardarán",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if respuesta == QMessageBox.StandardButton.Yes:
                self.overlay.hide()
        else:
            self.overlay.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overlay and self.overlay.isVisible():
            self.overlay.ajustar_a_padre()


