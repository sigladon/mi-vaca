from src.modelo.enums.tipos_transaccion import TiposTransaccion
from src.modelo.transaccion.transaccion import Transaccion
from src.vista.overlay import Overlay
from src.vista.ui.overlay_transacciones_ui import Ui_OverlayTransaccion


class OverlayTransaccion(Overlay):
    def __init__(self, parent=None):
        super().__init__(Ui_OverlayTransaccion(),parent)
        self._parent_ref = parent

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
