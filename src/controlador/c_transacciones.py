from enum import Enum

from PyQt6.QtCore import QObject, QDate
from PyQt6.QtWidgets import QComboBox

from src.modelo.entidades.usuario import Usuario
from src.modelo.enums.tipos_transaccion import TiposTransaccion
from src.modelo.transaccion.transacciones_list_model import TransaccionesListModel
from src.utils.manejador_archivos import ManejadorArchivos
from src.vista.overlay_presupuesto import OverlayPresupuesto
from src.vista.overlay_transacciones import OverlayTransaccion
from src.vista.panel_transacciones import PanelTransacciones


class CTransaccion(QObject):
    def __init__(self, vista: PanelTransacciones, usuario: Usuario):
        super().__init__()
        self._usuario = usuario
        self._vista = vista
        self._modelo_transacciones: TransaccionesListModel | None = None
        self.fecha_actual = QDate.currentDate()
        self._vista.overlay = OverlayTransaccion(self._vista)
        self._vista.ui.btn_registrar_transaccion.clicked.connect(self.mostrar_modal)
        self.llenar_combo(list(map(lambda t: t.value.nombre, TiposTransaccion)),self._vista.overlay.ui.cmb_tipo_transaccion)
        self._mostrar_cmb_presupuesto_meta(ocultar=True)
        self._vista.overlay.ui.cmb_tipo_transaccion.currentIndexChanged.connect(
            lambda index: self._mostrar_cmb_presupuesto_meta(es_ingreso=True) if index == 0 else self._mostrar_cmb_presupuesto_meta()
        )
        print(self._usuario.nombre)
        print(self._usuario.presupuestos)


    def _mostrar_cmb_presupuesto_meta(self, es_ingreso: bool = False, ocultar: bool = False):
        cmb_pm = self._vista.overlay.ui.cmb_presupuesto_meta
        lbl_pm = self._vista.overlay.ui.lbl_presupuesto_meta

        if ocultar:
            cmb_pm.hide()
            lbl_pm.hide()
            return

        cmb_pm.clear()
        if es_ingreso:
            lbl_pm.setText("Meta financiera")
            self.llenar_combo(list(map(lambda p: p.nombre, self._usuario.metas)), cmb_pm)
        else:
            lbl_pm.setText("Presupuesto")
            self.llenar_combo(list(map(lambda p: p.nombre, self._usuario.presupuestos)), cmb_pm)

        cmb_pm.show()
        lbl_pm.show()



    def mostrar_modal(self):
        self._vista.mostrar_modal()

    def set_modelo_transacciones(self, modelo):
        self._modelo_transacciones = modelo

    def llenar_combo(self,
                     lista: list, # Ahora recibimos (index, enum_member)
                     combobox: QComboBox):
        print("Llenando combo")
        print(lista)
        for index, item in enumerate(lista):
            print(item)
            combobox.addItem(item, index)

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
        self._usuario.agregar_transaccion(transaccion)
        if self._modelo_transacciones:
            self._modelo_transacciones.add_transaccion(transaccion)
        ManejadorArchivos.guardar_archivo(self._usuario.id_usuario, self._usuario)

    def actualizar_transaccion(self, transaccion_original, transaccion_editada):
        try:
            index = self._usuario.transacciones.index(transaccion_original)
            self._usuario.transacciones[index] = transaccion_editada
            self._modelo_transacciones.update_model()
            print("Transacción actualizada exitosamente.")
        except ValueError:
            print("No se pudo encontrar la transacción original para actualizar.")



