from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QMessageBox

from src.vista.overlay_transacciones import OverlayTransaccion
from src.vista.ui.panel_transacciones_ui import Ui_PanelTransacciones


class PanelTransacciones(QWidget):
    solicitar_mostrar_login = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.overlay: OverlayTransaccion | None = None
        self.ui = Ui_PanelTransacciones()
        self.ui.setupUi(self)
        self.ui.btn_registrar_transaccion.setFixedSize(300,60)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa; /* Fondo gris muy claro, casi blanco */
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }

            /* Estilos para el encabezado principal */
            QLabel#label { /* "Gestión de Transacciones" */
                font-size: 24px;
                font-weight: bold;
                color: #343a40; /* Gris oscuro para el título */
                margin-bottom: 5px;
            }

            QLabel#label_2 { /* "Registra y categoriza tus ingresos y gastos" */
                font-size: 14px;
                color: #6c757d; /* Gris más claro para la descripción */
                margin-bottom: 15px;
            }

            /* Estilo para el botón principal "Registrar Movimiento" */
            QPushButton#btn_registrar_transaccion {
                background-color: #007bff; /* Azul primario para acción principal */
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-left: 20px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            }

            QPushButton#btn_registrar_transaccion:hover {
                background-color: #0056b3; /* Azul más oscuro al pasar el ratón */
                box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.3);
            }
            QPushButton#btn_registrar_transaccion:pressed {
                background-color: #004085; /* Azul aún más oscuro al presionar */
            }

            /* Estilos para etiquetas de filtros */
            QLabel#lbl_tipo, QLabel#lbl_presupuesto_categoria, QLabel#lbl_categoria {
                font-size: 14px;
                color: #495057; /* Gris medio */
                padding-left: 5px; /* Pequeño padding para alinear con el combo box */
            }

            /* Estilos para los QComboBox (selectores de filtro) */
            QComboBox {
                padding: 8px 10px;
                border: 1px solid #ced4da; /* Borde suave */
                border-radius: 5px;
                font-size: 14px;
                background-color: #ffffff;
                selection-background-color: #007bff; /* Fondo azul al seleccionar */
                selection-color: white; /* Texto blanco al seleccionar */
            }

            QComboBox::drop-down {
                border: none;
                background-color: transparent;
                width: 25px; /* Ancho del botón de flecha */
            }

            QComboBox::down-arrow {
                image: url(./assets/iconos/arrow_down.svg); /* Asegúrate de tener este icono */
                width: 16px;
                height: 16px;
            }
            
            QComboBox:hover {
                border-color: #a8dadc; /* Borde más claro al pasar el ratón */
            }

            QComboBox:on { /* Cuando el combo box está abierto */
                border-color: #007bff;
            }

            /* Estilos para los botones de acción de filtros */
            QPushButton#btn_buscar_transacciones {
                background-color: #6c757d; /* Gris para botones secundarios */
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: normal;
                margin-top: 10px;
            }

            QPushButton#btn_buscar_transacciones:hover {
                background-color: #5a6268;
            }

            QPushButton#btn_limpiar_filtros {
                background-color: #dc3545; /* Rojo para botón de acción de "limpiar/peligro" */
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: normal;
                margin-top: 10px;
            }
            QPushButton#btn_limpiar_filtros:hover {
                background-color: #c82333;
            }

            /* Estilo para el título del historial */
            QLabel#label_3 { /* "Historial de Transacciones" */
                font-size: 18px;
                font-weight: bold;
                color: #343a40;
                margin-top: 20px;
                margin-bottom: 10px;
            }

            /* Estilos para la tabla de transacciones (QTableView) */
            QTableView {
                border: 1px solid #dee2e6; /* Borde general de la tabla */
                border-radius: 8px;
                gridline-color: #e9ecef; /* Color de las líneas de la cuadrícula */
                background-color: #ffffff;
                selection-background-color: #cfe2ff; /* Fondo para filas seleccionadas */
                selection-color: #343a40; /* Texto para filas seleccionadas */
            }

            QHeaderView::section { /* Estilo para los encabezados de la tabla */
                background-color: #e9ecef; /* Fondo de los encabezados */
                color: #495057; /* Color del texto del encabezado */
                padding: 8px;
                border: 1px solid #dee2e6;
                font-weight: bold;
                font-size: 14px;
            }

            QHeaderView::section:horizontal {
                border-bottom: 2px solid #007bff; /* Borde inferior azul para los encabezados */
            }

            QTableView::item { /* Estilo para las celdas individuales */
                padding: 6px;
                border: none; /* Eliminar bordes internos duplicados */
            }

            QTableView::item:selected {
                background-color: #cfe2ff; /* Color de fondo al seleccionar un ítem */
                color: #343a40; /* Color del texto al seleccionar un ítem */
            }

            /* Estilo para el área de scroll y scrollbar */
            QScrollArea {
                border: none; /* La tabla ya tiene su propio borde */
                background-color: transparent;
            }
            
            QScrollArea QWidget#scrollAreaWidgetContents {
                background-color: #ffffff; /* Asegura que el fondo del contenido sea blanco */
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
        """)

    def mostrar_modal(self, editando: bool = False):
        if editando:
            self.overlay.ui.btn_borrar_transaccion.show()
        else:
            self.overlay.ui.btn_borrar_transaccion.hide()

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
        self.overlay.ui.ptxt_notas_adicionales.clear()
        self.overlay.ui.txt_monto_transaccion.clear()
        self.overlay.ui.txt_descripcion_transaccion.clear()
        self.overlay.ui.cmb_tipo_transaccion.clear()
        self.overlay.ui.cmb_presupuesto_meta.clear()
        self.overlay.ui.cmb_categoria_transaccion.clear()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overlay and self.overlay.isVisible():
            self.overlay.ajustar_a_padre()
        # self._ui.btn_registrar_transaccion.clicked.connect(self.mostrar_modal)
        # self._llenar_combobox_mes_anio()
        # list(map(lambda item_index: self.agregarOpcion(item_index, self._ui.cmb_tipo_transaccion),
        #          enumerate(TiposTransaccion)))
        # self._ui.cmb_tipo_transaccion.currentIndexChanged.connect(lambda index: self._on_tipo_transaccion_seleccionado(index, self._ui.cmb_categoria_transaccion))

        # self._modelo_transacciones = TransaccionesListModel(self._usuario.transacciones)
        # self._modelo_proxy_transacciones = TransaccionesFilterProxyModel(self)
        # self._modelo_proxy_transacciones.setSourceModel(self._modelo_transacciones)
        # self._ui.lst_transacciones.setModel(self._modelo_proxy_transacciones)
        # self._controlador.set_modelo_transacciones(self._modelo_transacciones)

        # self._ui.btn_buscar_transacciones.clicked.connect(self._aplicar_filtros)
        # self._ui.btn_limpiar_filtros.clicked.connect(self.limpiar_filtros)
        # self._ui.lst_transacciones.clicked.connect(self._mostrar_ventana_edicion)

    # def mostrar_modal(self):
    #
    #     self.overlay = OverlayTransaccion(self._controlador, self)
    #     self.overlay.show()
    #
    # def ocultar_modal(self):
    #     self._modelo_transacciones.update_model()
    #     self._ui.lst_transacciones.update()
    #     self.overlay.hide()
    #
    #
    # def _on_tipo_transaccion_seleccionado(self, index: int, combobox):
    #     if index >= 0:
    #         selected_enum_member = self._ui.cmb_tipo_transaccion.itemData(index)
    #         if selected_enum_member == TiposTransaccion.INGRESO:
    #             combobox.clear()
    #             list(map(lambda item_index: self.agregarOpcion(item_index, combobox),
    #                      enumerate(CategoriasIngresos)))
    #         elif selected_enum_member == TiposTransaccion.EGRESO:
    #             combobox.clear()
    #             list(map(lambda item_index: self.agregarOpcion(item_index, combobox),
    #                      enumerate(CategoriasGastos)))
    #         else:
    #             combobox.clear()
    #             print("Ningún tipo de transacción válido seleccionado.")
    #
    # def _llenar_combobox_mes_anio(self):
    #     fecha_inicio = QDate(2025,1,1)
    #     fecha_actual = QDate.currentDate()
    #
    #     while fecha_actual >= fecha_inicio:
    #         texto = fecha_actual.toString("MMMM yyyy")
    #         valor = fecha_actual.toString("yyyy-MM")
    #         self._ui.cmb_mes_anio.addItem(texto.capitalize(), valor)
    #         fecha_actual = fecha_actual.addMonths(-1)
    #
    #
    # def _aplicar_filtros(self):
    #     mes_anio = self._ui.cmb_mes_anio.currentData()
    #     if mes_anio:
    #         anio, mes = map(int, mes_anio.split("-"))
    #         fecha_inicio = date(anio,mes,1)
    #         if mes == 12:
    #             fecha_fin = date(anio + 1,1,1) - timedelta(days=1)
    #         else:
    #             fecha_fin = date(anio,mes+1,1) - timedelta(days=1)
    #     else:
    #         fecha_inicio = fecha_fin = None
    #     self._modelo_proxy_transacciones.set_filter_dates(fecha_inicio, fecha_fin)
    #     tipo_filtro = self._ui.cmb_tipo_transaccion.currentData()
    #     self._modelo_proxy_transacciones.set_filter_type(tipo_filtro)
    #     categoria_filtro = self._ui.cmb_categoria_transaccion.currentData()
    #     self._modelo_proxy_transacciones.set_filter_category(categoria_filtro)
    #
    # def limpiar_filtros(self):
    #     self._ui.cmb_tipo_transaccion.setCurrentIndex(-1)
    #     self._ui.cmb_mes_anio.setCurrentIndex(-1)
    #     self._ui.cmb_categoria_transaccion.setCurrentIndex(-1)
    #     self._modelo_proxy_transacciones.set_filter_dates(None, None)
    #     self._modelo_proxy_transacciones.set_filter_type(None)
    #     self._modelo_proxy_transacciones.set_filter_category(None)
    #
    # def _mostrar_ventana_edicion(self, index: QModelIndex):
    #     transaccion = index.data(Qt.ItemDataRole.UserRole)
    #     if isinstance(transaccion, Transaccion):
    #         self.overlay.show()
    #     else:
    #         print("No se pudo cargar la transacción.")