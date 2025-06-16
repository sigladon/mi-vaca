from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QMessageBox

from src.vista.overlay_meta import OverlayMeta
from src.vista.ui.panel_metas_ui import Ui_PanelMetas


class PanelMetas(QWidget):
    solicitar_mostrar_login = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.overlay: OverlayMeta | None = None
        self.ui = Ui_PanelMetas()
        self.ui.setupUi(self)
        self.ui.btn_nueva_meta.clicked.connect(self.mostrar_modal)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa; /* Fondo gris muy claro */
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }

            /* Estilos para el encabezado principal */
            QLabel#label { /* "Metas Financieras" */
                font-size: 24px;
                font-weight: bold;
                color: #343a40; /* Gris oscuro para el título */
                margin-bottom: 5px;
            }

            QLabel#label_2 { /* "Define y rastrea tus objetivos de ahorro e inversión" */
                font-size: 14px;
                color: #6c757d; /* Gris más claro para la descripción */
                margin-bottom: 15px;
            }

            /* Estilo para el botón principal "Nueva Meta" */
            QPushButton#btn_nueva_meta {
                background-color: #17a2b8; /* Azul cian para acción principal de "meta" */
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-left: 20px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }

            QPushButton#btn_nueva_meta:hover {
                background-color: #138496; /* Azul cian más oscuro al pasar el ratón */
                box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.3);
            }
            QPushButton#btn_nueva_meta:pressed {
                background-color: #117a8b; /* Azul cian aún más oscuro al presionar */
            }
            
            /* Estilo para el área de scroll de metas individuales */
            QScrollArea {
                border: 1px solid #ced4da; /* Borde suave para el área de scroll */
                border-radius: 8px;
                background-color: #ffffff;
                margin-top: 15px; /* Espacio superior para separarlo del encabezado */
            }
            
            QScrollArea QWidget#scrollAreaWidgetContents {
                background-color: #ffffff; /* Asegura que el fondo del contenido sea blanco */
            }

            /* Estilo para la barra de desplazamiento */
            QScrollBar:vertical {
                border: none;
                background: #e9ecef;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #adb5bd;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }

            /* Puedes agregar estilos para el 'widget' dentro del scrollAreaWidgetContents aquí
               cuando empieces a poner contenido de cada meta. Por ejemplo: */
            /*
            QWidget#widget {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
            }
            */
        """)


    def mostrar_modal(self, editando: bool = False):
        if editando:
            self.overlay.ui.btn_borrar_meta.show()
        else:
            self.overlay.ui.btn_borrar_meta.hide()

        if self.overlay:
            self.overlay.show()

    def ocultar_modal(self, preguntar: bool = True):

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
                self.limpiar_formulario()
        else:
            self.overlay.hide()
            self.limpiar_formulario()

    def limpiar_formulario(self):
        self.overlay.ui.ptxt_descripcion.clear()
        self.overlay.ui.txt_nombre_meta.clear()
        self.overlay.ui.txt_monto_objetivo.clear()
        self.overlay.ui.txt_monto_actual.clear()
        self.overlay.ui.fch_limite.clear()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overlay and self.overlay.isVisible():
            self.overlay.ajustar_a_padre()


