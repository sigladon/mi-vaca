from src.vista.overlay import Overlay
from src.vista.ui.overlay_meta_ui import Ui_OverlayMeta


class OverlayMeta(Overlay):
    def __init__(self, parent=None):
        super().__init__(Ui_OverlayMeta(),parent)
        self.setStyleSheet("""
            QWidget#OverlayMeta { /* Estilos para la ventana/modal principal */
                background-color: rgba(255, 255, 255, 0.95); /* Fondo blanco semitransparente */
                border: 1px solid #ced4da;
                border-radius: 12px; /* Bordes más redondeados para un aspecto de modal */
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2); /* Sombra para que flote */
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }

            /* Estilos para el encabezado del modal */
            QLabel#label { /* "Crear Nueva Meta" */
                font-size: 22px;
                font-weight: bold;
                color: #343a40; /* Gris oscuro para el título */
                margin-bottom: 5px;
            }

            QLabel#label_7 { /* "Define un nuevo objetivo financiero" */
                font-size: 14px;
                color: #6c757d; /* Gris más claro para la descripción */
            }

            /* Botón de cerrar modal */
            QPushButton#btn_cerrar_modal {
                background-color: transparent;
                border: none;
                font-size: 20px;
                color: #6c757d;
                font-weight: bold;
                padding: 5px;
                border-radius: 20px; /* Completamente redondo */
            }

            QPushButton#btn_cerrar_modal:hover {
                background-color: #e9ecef;
                color: #495057;
            }

            /* Estilos para etiquetas de campos */
            QLabel#label_2, QLabel#label_3, QLabel#label_4, QLabel#label_5, QLabel#label_6 {
                font-size: 14px;
                color: #495057; /* Gris medio */
                margin-top: 10px; /* Espacio superior para separar las etiquetas de los campos */
                margin-bottom: 5px;
            }

            /* Estilos para QLineEdit (campos de texto) */
            QLineEdit {
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 8px; /* Bordes redondeados */
                font-size: 14px;
                background-color: #f8f9fa; /* Fondo ligeramente gris para los campos */
                color: #343a40;
            }

            QLineEdit:focus {
                border: 1px solid #17a2b8; /* Color azul cian al enfocar */
                background-color: #ffffff;
            }
            
            QLineEdit::placeholder {
                color: #adb5bd; /* Color del texto de placeholder */
            }

            /* Estilos para QPlainTextEdit (descripción) */
            QPlainTextEdit {
                min-height: 40px;  /* Altura mínima de 80 píxeles */
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f8f9fa;
                color: #343a40;
            }

            QPlainTextEdit:focus {
                border: 1px solid #17a2b8;
                background-color: #ffffff;
            }
            
            QPlainTextEdit::placeholder {
                color: #adb5bd;
            }

            /* Estilos para QDateEdit (selector de fecha) */
            QDateEdit {
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f8f9fa;
                color: #343a40;
                qproperty-calendarPopup: true; /* Asegura que el calendario emergente se vea bien */
            }

            QDateEdit:focus {
                border: 1px solid #17a2b8;
                background-color: #ffffff;
            }
            
            QDateEdit::drop-down {
                border: none;
                background-color: transparent;
                width: 25px;
            }
            
            QDateEdit::down-arrow {
                image: url(./assets/iconos/calendar.svg); /* Asegúrate de tener un icono de calendario */
                width: 18px;
                height: 18px;
            }
            QDateEdit::down-arrow:on { /* Cuando el calendario está abierto */
                image: url(./assets/iconos/calendar_filled.svg); /* Icono diferente si lo deseas */
            }
            
            /* Estilos para los botones de acción */
            QPushButton {
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 15px;
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            }

            QPushButton:hover {
                box-shadow: 0px 3px 8px rgba(0, 0, 0, 0.2);
            }

            QPushButton#btn_crear_meta {
                background-color: #17a2b8; /* Azul cian para acción positiva */
            }
            QPushButton#btn_crear_meta:hover {
                background-color: #138496;
            }
            QPushButton#btn_crear_meta:pressed {
                background-color: #117a8b;
            }

            QPushButton#btn_borrar_meta {
                background-color: #dc3545; /* Rojo para acción de borrar/peligro */
            }
            QPushButton#btn_borrar_meta:hover {
                background-color: #c82333;
            }
            QPushButton#btn_borrar_meta:pressed {
                background-color: #bb2d3b;
            }
        """)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)