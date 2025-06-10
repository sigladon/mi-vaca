from datetime import date, timedelta

from PyQt6.QtCore import pyqtSignal, Qt, QDate, QModelIndex
from PyQt6.QtWidgets import QWidget, QComboBox

from src.controlador.c_transacciones import CTransacciones
from src.modelo.enums.categorias_gastos import CategoriasGastos
from src.modelo.enums.categorias_ingresos import CategoriasIngresos
from src.modelo.enums.tipos_transaccion import TiposTransaccion
from src.modelo.transaccion import Transaccion
from src.modelo.transaccion.transacciones_filter_proxy_model import TransaccionesFilterProxyModel
from src.modelo.transaccion.transacciones_list_model import TransaccionesListModel
from src.modelo.transaccion.tipo_transaccion import TipoTransaccion
from src.vista.overlay_transacciones import OverlayTransaccion
from src.vista.ui.panel_transacciones_ui import Ui_PanelTransacciones


class PanelTransacciones(QWidget):
    solicitar_mostrar_login = pyqtSignal()
    def __init__(self, usuario):
        super().__init__()

        self.overlay = None
        self._usuario = usuario
        self._controlador = CTransacciones(self._usuario)
        self._ui = Ui_PanelTransacciones()
        self._ui.setupUi(self)
        self._ui.btn_registrar_transaccion.clicked.connect(self.mostrar_modal)
        self._llenar_combobox_mes_anio()
        list(map(lambda item_index: self.agregarOpcion(item_index, self._ui.cmb_tipo_transaccion),
                 enumerate(TiposTransaccion)))
        self._ui.cmb_tipo_transaccion.currentIndexChanged.connect(lambda index: self._on_tipo_transaccion_seleccionado(index, self._ui.cmb_categoria_transaccion))

        self._modelo_transacciones = TransaccionesListModel(self._usuario.transacciones)
        self._modelo_proxy_transacciones = TransaccionesFilterProxyModel(self)
        self._modelo_proxy_transacciones.setSourceModel(self._modelo_transacciones)
        self._ui.lst_transacciones.setModel(self._modelo_proxy_transacciones)
        self._controlador.set_modelo_transacciones(self._modelo_transacciones)

        self._ui.btn_buscar_transacciones.clicked.connect(self._aplicar_filtros)
        self._ui.btn_limpiar_filtros.clicked.connect(self.limpiar_filtros)
        self._ui.lst_transacciones.clicked.connect(self._mostrar_ventana_edicion)

    def mostrar_modal(self):

        self.overlay = OverlayTransaccion(self._controlador, self)
        self.overlay.show()

    def ocultar_modal(self):
        self._modelo_transacciones.update_model()
        self._ui.lst_transacciones.update()
        self.overlay.hide()

    def agregarOpcion(self,
                      item_data: tuple[int, TiposTransaccion], # Ahora recibimos (index, enum_member)
                      combobox: QComboBox):
        index, tipo_enum_member = item_data
        tipo_transaccion_data: TipoTransaccion = tipo_enum_member.value

        combobox.addItem(tipo_transaccion_data.nombre, tipo_enum_member)
        combobox.setItemData(index, tipo_transaccion_data.descripcion, Qt.ItemDataRole.ToolTipRole)

    def _on_tipo_transaccion_seleccionado(self, index: int, combobox):
        if index >= 0:
            selected_enum_member = self._ui.cmb_tipo_transaccion.itemData(index)
            if selected_enum_member == TiposTransaccion.INGRESO:
                combobox.clear()
                list(map(lambda item_index: self.agregarOpcion(item_index, combobox),
                         enumerate(CategoriasIngresos)))
            elif selected_enum_member == TiposTransaccion.EGRESO:
                combobox.clear()
                list(map(lambda item_index: self.agregarOpcion(item_index, combobox),
                         enumerate(CategoriasGastos)))
            else:
                combobox.clear()
                print("Ningún tipo de transacción válido seleccionado.")

    def _llenar_combobox_mes_anio(self):
        fecha_inicio = QDate(2025,1,1)
        fecha_actual = QDate.currentDate()

        while fecha_actual >= fecha_inicio:
            texto = fecha_actual.toString("MMMM yyyy")
            valor = fecha_actual.toString("yyyy-MM")
            self._ui.cmb_mes_anio.addItem(texto.capitalize(), valor)
            fecha_actual = fecha_actual.addMonths(-1)


    def _aplicar_filtros(self):
        mes_anio = self._ui.cmb_mes_anio.currentData()
        if mes_anio:
            anio, mes = map(int, mes_anio.split("-"))
            fecha_inicio = date(anio,mes,1)
            if mes == 12:
                fecha_fin = date(anio + 1,1,1) - timedelta(days=1)
            else:
                fecha_fin = date(anio,mes+1,1) - timedelta(days=1)
        else:
            fecha_inicio = fecha_fin = None
        self._modelo_proxy_transacciones.set_filter_dates(fecha_inicio, fecha_fin)
        tipo_filtro = self._ui.cmb_tipo_transaccion.currentData()
        self._modelo_proxy_transacciones.set_filter_type(tipo_filtro)
        categoria_filtro = self._ui.cmb_categoria_transaccion.currentData()
        self._modelo_proxy_transacciones.set_filter_category(categoria_filtro)

    def limpiar_filtros(self):
        self._ui.cmb_tipo_transaccion.setCurrentIndex(-1)
        self._ui.cmb_mes_anio.setCurrentIndex(-1)
        self._ui.cmb_categoria_transaccion.setCurrentIndex(-1)
        self._modelo_proxy_transacciones.set_filter_dates(None, None)
        self._modelo_proxy_transacciones.set_filter_type(None)
        self._modelo_proxy_transacciones.set_filter_category(None)

    def _mostrar_ventana_edicion(self, index: QModelIndex):
        transaccion = index.data(Qt.ItemDataRole.UserRole)
        if isinstance(transaccion, Transaccion):
            self.overlay = OverlayTransaccion(self._controlador, self, transaccion=transaccion)
            self.overlay.show()
        else:
            print("No se pudo cargar la transacción.")