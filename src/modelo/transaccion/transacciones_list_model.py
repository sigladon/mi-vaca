from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt
from src.modelo.transaccion.transaccion import Transaccion


class TransaccionesListModel(QAbstractListModel):
    def __init__(self, transacciones: list[Transaccion] = None, parent=None):
        super().__init__(parent)
        self._transacciones = transacciones

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None # Índice inválido

        transaccion = self._transacciones[index.row()] # Obtén el objeto Transaccion

        if role == Qt.ItemDataRole.DisplayRole:
            return (f"{transaccion.fecha.strftime('%Y-%m-%d')} - "
                    f"{transaccion.tipo.name}: "
                    f"{transaccion.descripcion} - ${transaccion.monto:.2f}")

        if role == Qt.ItemDataRole.UserRole:
            return transaccion

        return None # Rol no manejado

    def rowCount(self, parent: QModelIndex = QModelIndex()):
        return len(self._transacciones)

    def add_transaccion(self, transaccion: Transaccion):
        self.beginResetModel()
        # self._transacciones.sort(key=lambda t: t.fecha, reverse=True)
        self.endResetModel()

    def update_model(self):
        self.beginResetModel()
        # self._transacciones.sort(key=lambda t: t.fecha, reverse=True)
        self.endResetModel()

    def get_transaccion_by_index(self, index: QModelIndex) -> Transaccion | None:
        if not index.isValid() or index.row() >= len(self._transacciones) or index.row() < 0:
            return None
        return self._transacciones[index.row()]

    def set_transacciones(self, nuevas_transacciones: list[Transaccion]):
        self.beginResetModel()
        self._transacciones = sorted(nuevas_transacciones, key=lambda t: t.fecha, reverse=True)
        self.endResetModel()