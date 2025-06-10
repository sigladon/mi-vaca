from PyQt6.QtCore import QObject, QDate

from src.modelo.transaccion.transacciones_list_model import TransaccionesListModel
from src.utils.manejador_archivos import ManejadorArchivos


class CTransacciones(QObject):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self._modelo_transacciones: TransaccionesListModel | None = None
        self.fecha_actual = QDate.currentDate()

    def set_modelo_transacciones(self, modelo):
        self._modelo_transacciones = modelo

    def verificar_monto(self, monto, txt_monto):
        try:
            monto = float(monto)
            if monto <= 0:
                txt_monto.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
                print("El monto debe ser mayor a 0")
                return False
            else:
                txt_monto.setStyleSheet("")
                return True
        except ValueError:
            txt_monto.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            print("El monto debe ser un número")
            return False

    def verificar_descripcion(self, descripcion, txt_descripcion):
        descripcion = descripcion.strip()
        if descripcion == "":
            txt_descripcion.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            print("La descripción no puede estar vacía")
            return False
        else:
            txt_descripcion.setStyleSheet("")
            return True

    def verificar_combo(self, combobox):
        if combobox.currentIndex() == -1:
            combobox.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            print("Debe seleccionar al menos una opción")
            return False
        else:
            combobox.setStyleSheet("")
            return True

    def guardar_transaccion(self, transaccion):
        self.usuario.agregar_transaccion(transaccion)
        if self._modelo_transacciones:
            self._modelo_transacciones.add_transaccion(transaccion)
        ManejadorArchivos.guardar_archivo(self.usuario.id_usuario,self.usuario)

    def actualizar_transaccion(self, transaccion_original, transaccion_editada):
        try:
            index = self.usuario.transacciones.index(transaccion_original)
            self.usuario.transacciones[index] = transaccion_editada
            self._modelo_transacciones.update_model()
            print("Transacción actualizada exitosamente.")
        except ValueError:
            print("No se pudo encontrar la transacción original para actualizar.")



