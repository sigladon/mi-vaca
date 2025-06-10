from PyQt6.QtCore import QSortFilterProxyModel, QModelIndex, Qt
from datetime import date

from src.modelo.enums.categorias_gastos import CategoriasGastos
from src.modelo.enums.categorias_ingresos import CategoriasIngresos
from src.modelo.enums.tipos_transaccion import TiposTransaccion
from src.modelo.transaccion.transaccion import Transaccion


class TransaccionesFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Atributos para almacenar los criterios de filtro
        self._filter_start_date: date | None = None
        self._filter_end_date: date | None = None
        self._filter_type: TiposTransaccion | None = None
        self._filter_category: CategoriasGastos | CategoriasIngresos | None = None # Asumimos la categoría como string

    def set_filter_dates(self, start_date: date | None, end_date: date | None):
        self._filter_start_date = start_date
        self._filter_end_date = end_date
        self.invalidateFilter() # Invalida el filtro para que se vuelva a aplicar

    def set_filter_type(self, transaccion_type: TiposTransaccion | None):
        self._filter_type = transaccion_type
        self.invalidateFilter() # Invalida el filtro

    def set_filter_category(self, category: CategoriasIngresos | CategoriasGastos | None):
        self._filter_category = category
        self.invalidateFilter() # Invalida el filtro

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        source_index = self.sourceModel().index(source_row, 0, source_parent)
        if not source_index.isValid():
            return True

        transaccion: Transaccion = self.sourceModel().data(source_index, Qt.ItemDataRole.UserRole)

        if transaccion is None:
            return False

        if self._filter_start_date and transaccion.fecha < self._filter_start_date:
            return False
        if self._filter_end_date and transaccion.fecha > self._filter_end_date:
            return False

        if self._filter_type is not None and transaccion.tipo != self._filter_type:
            return False

        if self._filter_category is not None and transaccion.categoria != self._filter_category:
            return False

        return True