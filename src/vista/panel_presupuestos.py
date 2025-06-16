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
        self.ui.btn_agregar_presupuesto.setFixedSize(300, 60)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa; /* Un gris muy claro, casi blanco */
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }

            /* Estilos para el encabezado principal */
            QLabel#label { /* "Gestión de Presupuestos" */
                font-size: 24px;
                font-weight: bold;
                color: #343a40; /* Gris oscuro para el título */
                margin-bottom: 5px;
            }

            QLabel#label_2 { /* "Crea y monitorea tus presupuestos mensuales" */
                font-size: 14px;
                color: #6c757d; /* Gris más claro para la descripción */
                margin-bottom: 15px;
            }

            /* Estilo para el botón principal "Nuevo Presupuesto" */
            QPushButton#btn_agregar_presupuesto {
                background-color: #28a745; /* Verde vibrante para acción positiva */
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px; /* Bordes más redondeados */
                font-size: 16px;
                font-weight: bold;
                margin-left: 20px; /* Espacio a la izquierda del texto */
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Sombra sutil */
            }

            QPushButton#btn_agregar_presupuesto:hover {
                background-color: #218838; /* Verde más oscuro al pasar el ratón */
                box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.3); /* Sombra más pronunciada */
            }
            
            QPushButton#btn_agregar_presupuesto:pressed {
                background-color: #1e7e34; /* Verde aún más oscuro al presionar */
            }

            /* Estilos para los "cards" de estadísticas (Total, Activos, Límite) */
            QGraphicsView { /* Usaremos QGraphicsView como "card" de fondo para los iconos */
                background-color: #ffffff; /* Fondo blanco para las tarjetas */
                border: 1px solid #e9ecef; /* Borde muy sutil */
                border-radius: 8px;
                padding: 5px;
            }
            
            /* Estilos para los contenedores de las estadísticas individuales */
            QHBoxLayout { /* Esto puede aplicarse si el QHBoxLayout es un widget directo, si no, se podría usar un QFrame */
                spacing: 10px; /* Espacio entre el icono y el texto */
                border: 1px solid #dee2e6; /* Borde para el contenedor completo */
                border-radius: 8px;
                padding: 10px;
                background-color: #ffffff;
                margin: 5px; /* Espacio entre los bloques de estadísticas */
            }

            /* Estilos para las etiquetas de las estadísticas (ej. "Total Presupuestos") */
            QLabel#label_3, QLabel#label_5, QLabel#label_7 {
                font-size: 13px;
                color: #495057; /* Gris medio para las etiquetas */
                font-weight: 500; /* Un poco más de peso que lo normal */
                margin-bottom: 2px; /* Espacio entre el título y el valor */
            }

            /* Estilos para los valores de las estadísticas (ej. "1", "1", "1") */
            QLabel#lbl_total_presupuestos, QLabel#lbl_presupuestos_activos, QLabel#lbl_limite_total {
                font-size: 20px; /* Tamaño grande para los valores */
                font-weight: bold;
                color: #007bff; /* Color azul primario para los valores */
            }
            
            /* Estilo para el área de scroll de presupuestos individuales */
            QScrollArea {
                border: 1px solid #ced4da; /* Borde para el área de scroll */
                border-radius: 8px;
                background-color: #ffffff;
            }
            
            QScrollArea QWidget#scrollAreaWidgetContents {
                background-color: #ffffff; /* Fondo blanco para el contenido del scroll */
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
        """)
        # self.ui.btn_agregar_presupuesto.setStyleSheet("""
        #     QPushButton {
        #         background-color: #ff8904;
        #         color: white;
        #         border: none;
        #         border-radius: 6px;
        #         font-weight: 500;
        #         font-size: 13px;
        #         padding: 0;
        #     }
        #     QPushButton:hover {
        #         background-color: #f08628;
        #     }
        #     QPushButton:pressed {
        #         background-color: #fe9e54;
        #     }
        # """)

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


