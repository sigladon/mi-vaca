from src.vista.overlay import Overlay
from src.vista.ui.overlay_transacciones_ui import Ui_OverlayTransaccion


class OverlayTransaccion(Overlay):
    def __init__(self, parent=None):
        super().__init__(Ui_OverlayTransaccion(),parent)
        self._parent_ref = parent
        self.setStyleSheet("""
            QWidget#OverlayTransaccion { /* Estilos para la ventana/modal principal */
                background-color: rgba(255, 255, 255, 0.95); /* Fondo blanco semitransparente */
                border: 1px solid #ced4da;
                border-radius: 12px; /* Bordes más redondeados para un aspecto de modal */
                padding: 20px; /* Padding general dentro del modal */
            }

            /* Estilos para el encabezado del modal */
            QLabel#label { /* "Agregar Transacción" */
                padding: 0;
                font-size: 16px;
                font-weight: bold;
                color: #343a40; /* Gris oscuro para el título */
                margin-bottom: 5px;
            }

            QLabel#label_2 { /* "Registra un nuevo ingreso o gasto" */
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

            /* Estilos para etiquetas de campos (general) */
            QLabel {
                font-size: 14px;
                color: #495057; /* Gris medio */
                margin-top: 10px; /* Espacio superior para separar las etiquetas de los campos */
                margin-bottom: 5px;
            }
            
            /* Ajuste específico para las etiquetas en el FormLayout si es necesario */
            QFormLayout QLabel {
                padding-top: 5px; /* Un poco de padding para que el texto no esté pegado al borde superior del campo */
            }

            /* Estilos para QLineEdit (campos de texto) */
            QLineEdit {
                min-height: 20px;  /* Altura mínima de 80 píxeles */
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 8px; /* Bordes redondeados */
                font-size: 14px;
                background-color: #f8f9fa; /* Fondo ligeramente gris para los campos */
                color: #343a40;
            }

            QLineEdit:focus {
                border: 1px solid #fd7e14; /* Naranja para el enfoque (transacciones) */
                background-color: #ffffff;
            }
            
            QLineEdit::placeholder {
                color: #adb5bd; /* Color del texto de placeholder */
            }

            /* Estilos para QComboBox (selectores) */
            QComboBox {
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f8f9fa;
                color: #343a40;
                selection-background-color: #fd7e14; /* Naranja al seleccionar */
                selection-color: white;
            }

            QComboBox::drop-down {
                border: none;
                background-color: transparent;
                width: 25px;
            }

            QComboBox::down-arrow {
                image: url(./assets/iconos/arrow_down.svg); /* Asegúrate de tener este icono */
                width: 16px;
                height: 16px;
            }
            
            QComboBox:hover {
                border-color: #a8dadc;
            }

            QComboBox:on { /* Cuando el combo box está abierto */
                border-color: #fd7e14;
            }

            /* Estilos para QDateEdit (selector de fecha) */
            QDateEdit {
                min-height: 20px;  /* Altura mínima de 80 píxeles */
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f8f9fa;
                color: #343a40;
                qproperty-calendarPopup: true;
            }

            QDateEdit:focus {
                border: 1px solid #fd7e14;
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
                border: 1px solid #fd7e14;
                background-color: #ffffff;
            }
            
            QPlainTextEdit::placeholder {
                color: #adb5bd;
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
            }

            QPushButton:hover {
            }

            QPushButton#btn_guardar_transaccion {
                background-color: #20c997; /* Un verde turquesa vibrante para acción positiva */
            }
            QPushButton#btn_guardar_transaccion:hover {
                background-color: #17a2b8; /* Cambia a azul cian en hover */
            }
            QPushButton#btn_guardar_transaccion:pressed {
                background-color: #138496;
            }

            QPushButton#btn_borrar_transaccion {
                background-color: #dc3545; /* Rojo para acción de borrar/peligro */
            }
            QPushButton#btn_borrar_transaccion:hover {
                background-color: #c82333;
            }
            QPushButton#btn_borrar_transaccion:pressed {
                background-color: #bb2d3b;
            }
        """)

    #     self.ui.fch_transaccion.setDate(self._controlador.fecha_actual)
    #
    #
    #
    #     list(map(lambda item_index: parent.agregarOpcion(item_index, self.ui.cmb_tipo_transaccion),
    #              enumerate(TiposTransaccion)))
    #     self.ui.cmb_tipo_transaccion.currentIndexChanged.connect(lambda index: parent._on_tipo_transaccion_seleccionado(index, self.ui.cmb_categoria_transaccion))
    #     self.ui.btn_guardar_transaccion.clicked.connect(self.guardar_transaccion)
    #
    # def cargar_datos_edicion(self):
    #     self.ui.cmb_tipo_transaccion.setCurrentIndex(
    #         self.ui.cmb_tipo_transaccion.findData(self._transaccion.tipo)
    #     )
    #
    #     # Forzar el llenado de categorías después de tipo
    #     self._parent_ref._on_tipo_transaccion_seleccionado(
    #         self.ui.cmb_tipo_transaccion.currentIndex(), self.ui.cmb_categoria_transaccion
    #     )
    #
    #     self.ui.cmb_categoria_transaccion.setCurrentIndex(
    #         self.ui.cmb_categoria_transaccion.findData(self._transaccion.categoria)
    #     )
    #
    #     self.ui.txt_monto_transaccion.setText(str(self._transaccion.monto))
    #     self.ui.txt_descripcion_transaccion.setText(self._transaccion.descripcion)
    #     self.ui.fch_transaccion.setDate(self._transaccion.fecha)
    #     self.ui.ptxt_notas_adicionales.setPlainText(self._transaccion.notas)
    #
    # def resizeEvent(self, a0):
    #     super().resizeEvent(a0)
    #
    # def guardar_transaccion(self):
    #     tipo = self.ui.cmb_tipo_transaccion.currentData()
    #     monto = self.ui.txt_monto_transaccion.text().strip()
    #     descripcion = self.ui.txt_descripcion_transaccion.text().strip()
    #     categoria = self.ui.cmb_categoria_transaccion.currentData()
    #     fecha = self.ui.fch_transaccion.date().toPyDate()
    #     notas = self.ui.ptxt_notas_adicionales.toPlainText().strip()
    #
    #     if (self._controlador.verificar_descripcion(descripcion, self.ui.txt_descripcion_transaccion)
    #             and self._controlador.verificar_monto(monto, self.ui.txt_monto_transaccion)
    #             and self._controlador.verificar_combo(self.ui.cmb_tipo_transaccion)
    #             and self._controlador.verificar_combo(self.ui.cmb_categoria_transaccion)):
    #
    #         if self._transaccion is None:
    #             nueva_transaccion = Transaccion(
    #                 tipo, float(monto), descripcion, categoria, fecha, notas
    #             )
    #             self._controlador.guardar_transaccion(nueva_transaccion)
    #             print("Se guardó la transacción exitosamente")
    #         else:
    #             # Modificar la transacción existente
    #             transaccion_editada = Transaccion(
    #                 tipo, float(monto), descripcion, categoria, fecha, notas
    #             )
    #             self._controlador.actualizar_transaccion(self._transaccion, transaccion_editada)
    #
    #             print("Se actualizó la transacción exitosamente")
    #
    #         self._parent_ref.ocultar_modal()
