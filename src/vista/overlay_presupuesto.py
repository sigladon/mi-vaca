from src.vista.overlay import Overlay
from src.vista.ui.overlay_presupuesto_ui import Ui_OverlayPresupuesto


class OverlayPresupuesto(Overlay):
    def __init__(self, parent=None):
        super().__init__(Ui_OverlayPresupuesto(),parent)
        self.setStyleSheet("""
            QWidget#OverlayPresupuesto { /* Estilos para la ventana/modal principal */
                background-color: rgba(255, 255, 255, 0.95); /* Fondo blanco semitransparente */
                border: 1px solid #ced4da;
                border-radius: 12px; /* Bordes más redondeados para un aspecto de modal */
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2); /* Sombra para que flote */
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }

            /* Estilos para el título del modal */
            QLabel#lbl_nombre_modal {
                font-size: 22px;
                font-weight: bold;
                color: #343a40; /* Gris oscuro para el título */
                margin-bottom: 10px;
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

            /* Estilos para el área de scroll y scrollbar */
            QScrollArea {
                border: none; /* No queremos un borde para el scrollArea en sí */
                background-color: transparent;
            }
            
            QScrollArea QWidget#scrollAreaWidgetContents {
                background-color: transparent; /* El contenido no necesita fondo propio */
            }

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

            /* Estilos para etiquetas de campos (general) */
            QLabel {
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
                border: 1px solid #28a745; /* Color verde para el enfoque (presupuesto) */
                background-color: #ffffff;
            }
            
            QLineEdit::placeholder {
                color: #adb5bd; /* Color del texto de placeholder */
            }

            /* Estilos para QDateEdit (selector de fecha) */
            QDateEdit {
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f8f9fa;
                color: #343a40;
                qproperty-calendarPopup: true;
            }

            QDateEdit:focus {
                border: 1px solid #28a745;
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

            /* Botón "Agregar" categoría */
            QPushButton#btn_agregar_categoria {
                background-color: #17a2b8; /* Azul cian para acción de agregar */
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                margin-left: 5px; /* Espacio con el campo de texto */
            }
            
            QPushButton#btn_agregar_categoria:hover {
                background-color: #138496;
            }

            /* Contenedor para categorías añadidas dinámicamente */
            QWidget#contenedor_categoria {
                /* background-color: #f1f3f5; */ /* Puedes darle un fondo si quieres resaltarlo */
                border: 1px dashed #ced4da; /* Borde punteado para indicar un área de contenido */
                border-radius: 8px;
                padding: 10px;
                margin-top: 10px;
            }
            
            /* Estilos para QPlainTextEdit (notas) */
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
                border: 1px solid #28a745;
                background-color: #ffffff;
            }
            
            QPlainTextEdit::placeholder {
                color: #adb5bd;
            }

            /* Estilos para QCheckBox (notificaciones) */
            QCheckBox {
                font-size: 14px;
                color: #343a40;
                margin-top: 15px;
                padding-left: 5px; /* Ajusta el padding para alinear el texto */
            }

            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: #ffffff;
            }

            QCheckBox::indicator:checked {
                background-color: #28a745; /* Verde cuando está marcado */
                border: 1px solid #28a745;
                image: url(./assets/iconos/check.svg); /* Icono de check (asegúrate de tenerlo) */
            }

            QCheckBox::indicator:hover {
                border-color: #a8dadc;
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

            QPushButton#btn_crear_presupuesto {
                background-color: #28a745; /* Verde para acción positiva (crear/guardar) */
            }
            QPushButton#btn_crear_presupuesto:hover {
                background-color: #218838;
            }
            QPushButton#btn_crear_presupuesto:pressed {
                background-color: #1e7e34;
            }

            QPushButton#btn_borrar_presupuesto {
                background-color: #dc3545; /* Rojo para acción de borrar/peligro */
            }
            QPushButton#btn_borrar_presupuesto:hover {
                background-color: #c82333;
            }
            QPushButton#btn_borrar_presupuesto:pressed {
                background-color: #bb2d3b;
            }
        """)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)