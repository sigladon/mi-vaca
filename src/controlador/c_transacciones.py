from datetime import date
from decimal import Decimal, InvalidOperation
from typing import List

from PyQt6.QtCore import QObject, QDate, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QComboBox, QLineEdit, QHeaderView, QMessageBox

from src.controlador.c_presupuestos import CPresupuestos
from src.modelo.entidades.movimiento import Movimiento
from src.modelo.entidades.usuario import Usuario
from src.modelo.enums.tipos_transaccion import TiposTransaccion
from src.utils.manejador_archivos import ManejadorArchivos
from src.vista.overlay_transacciones import OverlayTransaccion
from src.vista.panel_transacciones import PanelTransacciones


class CTransaccion(QObject):
    def __init__(self, vista: PanelTransacciones, usuario: Usuario):
        super().__init__()
        self._modelo_transacciones = None
        self.categoria_valido = None
        self.presupuesto_meta_valido = None
        self.tipo_movimiento_valido = None
        self.descripcion_valida = None
        self.monto_valido = None
        self._usuario = usuario
        self._vista = vista
        self.modelo_tabla = None
        self.fecha_actual = QDate.currentDate()
        self._vista.overlay = OverlayTransaccion(self._vista)

        # Variables para modo edición
        self.modo_edicion = False
        self.movimiento_editando = None

        self._vista.ui.btn_registrar_transaccion.clicked.connect(self.mostrar_modal)
        # self.cargar_transacciones_en_tabla()
        self._vista.overlay.ui.btn_guardar_transaccion.clicked.connect(self.guardar_transaccion)
        self.inicializar_filtros()

    def validar_categoria(self):
        self.categoria_valido = True

    def verificar_descripcion(self):
        txt_desc: QLineEdit = self.sender()
        desc = txt_desc.text()
        if desc == "":
            txt_desc.setStyleSheet("")
            self.descripcion_valida = False
        elif not CPresupuestos.validar_nombre(desc):
            print("El nombre del presupuesto no es válido") # Para depuración
            txt_desc.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.descripcion_valida = False
        else:
            txt_desc.setStyleSheet("")
            self.descripcion_valida = True

    def _mostrar_cmb_presupuesto_meta(self, ocultar: bool = False):
        cmb_pm = self._vista.overlay.ui.cmb_presupuesto_meta
        lbl_pm = self._vista.overlay.ui.lbl_presupuesto_meta
        self.tipo_movimiento_valido = True
        self.presupuesto_meta_valido = False
        self.categoria_valido = False

        if ocultar:
            cmb_pm.hide()
            lbl_pm.hide()
            cmb_pm.clear()
            self._mostrar_cmb_categoria()
            self.presupuesto_meta_valido = True
            self.categoria_valido = True
            return

        cmb_pm.clear()
        self.llenar_combo(list(map(lambda p: p.nombre, filter(lambda p: p.esta_activo,self._usuario.presupuestos))), cmb_pm)
        self.llenar_combo(list(map(lambda m: m.nombre, filter(lambda m: m.esta_activo, self._usuario.metas))), cmb_pm)

        cmb_pm.show()
        lbl_pm.show()

    def limitar_fecha(self, fecha_minima: date, fecha_maxima: date):
        fch_fecha_transaccion = self._vista.overlay.ui.fch_transaccion
        fch_fecha_transaccion.setMinimumDate(fecha_minima)
        fch_fecha_transaccion.setMaximumDate(fecha_maxima)

    def _mostrar_cmb_categoria(self, index: int = -1):
        cmb_cat = self._vista.overlay.ui.cmb_categoria_transaccion
        lbl_cat = self._vista.overlay.ui.lbl_categoria_transaccion
        cantidad_presupuestos = len(self._usuario.presupuestos)
        self.presupuesto_meta_valido = True
        self.categoria_valido = False

        if index == -1:
            cmb_cat.hide()
            lbl_cat.hide()
            self.categoria_valido = True
            return
        elif index >= cantidad_presupuestos:
            meta = self._usuario.metas[cantidad_presupuestos - index -1]
            self.limitar_fecha(meta.fecha_inicio, meta.fecha_limite)
            cmb_cat.hide()
            lbl_cat.hide()
            self.categoria_valido = True
            return

        presupuesto = self._usuario.presupuestos[index]
        self.limitar_fecha(presupuesto.inicio_presupuesto, presupuesto.fin_presupuesto)
        categorias = presupuesto.categorias
        cmb_cat.clear()
        self.llenar_combo(list(categorias.keys()), cmb_cat)
        self.categoria_valido = False

        cmb_cat.show()
        lbl_cat.show()

    def cargar_combos(self):
        self.llenar_combo(list(map(lambda t: t.value.nombre, TiposTransaccion)),self._vista.overlay.ui.cmb_tipo_transaccion)
        self._mostrar_cmb_presupuesto_meta(ocultar=True)
        self._vista.overlay.ui.cmb_tipo_transaccion.currentIndexChanged.connect(
            lambda index: self._mostrar_cmb_presupuesto_meta(ocultar=True) if index == 0 else self._mostrar_cmb_presupuesto_meta()
        )
        self._vista.overlay.ui.cmb_presupuesto_meta.currentIndexChanged.connect(
            lambda index: self._mostrar_cmb_categoria(index)
        )
        self._vista.overlay.ui.cmb_categoria_transaccion.currentIndexChanged.connect(self.validar_categoria)
        self._vista.overlay.ui.fch_transaccion.setDate(QDate().currentDate())
        self._vista.overlay.ui.txt_monto_transaccion.editingFinished.connect(self.verificar_monto)
        self._vista.overlay.ui.txt_descripcion_transaccion.editingFinished.connect(self.verificar_descripcion)
        self._mostrar_cmb_categoria()

    def mostrar_modal(self):
        """Muestra el modal para crear una nueva transacción"""
        self.modo_edicion = False
        self.movimiento_editando = None
        self._limpiar_formulario()
        self.cargar_combos()
        self._vista.mostrar_modal()

    def mostrar_modal_edicion(self, movimiento: Movimiento):
        """Muestra el modal para editar una transacción existente"""
        self.modo_edicion = True
        self.movimiento_editando = movimiento
        self._limpiar_formulario()
        self.cargar_combos()
        self.actualizar_banderas(True)
        self._cargar_datos_movimiento(movimiento)
        self._vista.mostrar_modal(True)
        self._vista.overlay.ui.btn_borrar_transaccion.clicked.connect(
            lambda: self.borrar_movimiento(movimiento)
        )
        print("Se mostró el modal")

    def borrar_movimiento(self, movimiento: Movimiento):
        respuesta = QMessageBox.question(
            self._vista.overlay,
            "Confirmar eliminación",
            f"̉¿Estás seguro de que quieres eliminar este presupuesto?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            id_movimiento = movimiento.id
            self._usuario.movimientos.remove(movimiento)
            ManejadorArchivos.guardar_archivo(self._usuario.id, self._usuario)
            self.actualizar_banderas()
            self.cargar_transacciones_en_tabla()
            self._vista.ocultar_modal(False)

    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self._vista.overlay.ui.txt_descripcion_transaccion.clear()
        self._vista.overlay.ui.txt_monto_transaccion.clear()
        self._vista.overlay.ui.ptxt_notas_adicionales.clear()
        self._vista.overlay.ui.fch_transaccion.setDate(QDate.currentDate())
        self._vista.overlay.ui.cmb_tipo_transaccion.setCurrentIndex(0)
        self._vista.overlay.ui.cmb_presupuesto_meta.setCurrentIndex(-1)
        self._vista.overlay.ui.cmb_categoria_transaccion.setCurrentIndex(-1)

        # Resetear validaciones
        self.actualizar_banderas(False)

    def _cargar_datos_movimiento(self, movimiento: Movimiento):
        """Carga los datos del movimiento en el formulario para edición"""
        # Cargar datos básicos
        self._vista.overlay.ui.txt_descripcion_transaccion.setText(movimiento.descripcion)
        self._vista.overlay.ui.txt_monto_transaccion.setText(str(movimiento.monto))
        self._vista.overlay.ui.ptxt_notas_adicionales.setPlainText(movimiento.notas or "")
        self._vista.overlay.ui.fch_transaccion.setDate(QDate.fromString(
            movimiento.fecha_transaccion.isoformat(), Qt.DateFormat.ISODate))

        # Configurar tipo de transacción
        if movimiento.tipo_movimiento == TiposTransaccion.INGRESO:
            self._vista.overlay.ui.cmb_tipo_transaccion.setCurrentIndex(0)
        else:
            self._vista.overlay.ui.cmb_tipo_transaccion.setCurrentIndex(1)

            # Si es egreso, buscar el presupuesto o meta asociada
            self._cargar_presupuesto_meta_asociado(movimiento)

        # Validar campos cargados

    def _cargar_presupuesto_meta_asociado(self, movimiento: Movimiento):
        """Busca y carga el presupuesto o meta asociado al movimiento"""
        # Buscar en presupuestos
        for i, presupuesto in enumerate(self._usuario.presupuestos):
            if (movimiento.id in presupuesto.movimientos or
                    (movimiento.categoria and movimiento.categoria in presupuesto.categorias)):
                self._vista.overlay.ui.cmb_presupuesto_meta.setCurrentIndex(i)

                # Si tiene categoría, seleccionarla
                if movimiento.categoria:
                    categorias = list(presupuesto.categorias.keys())
                    if movimiento.categoria in categorias:
                        indice_categoria = categorias.index(movimiento.categoria)
                        self._vista.overlay.ui.cmb_categoria_transaccion.setCurrentIndex(indice_categoria)
                return

        # Buscar en metas
        cantidad_presupuestos = len(self._usuario.presupuestos)
        for i, meta in enumerate(self._usuario.metas):
            if movimiento.id in meta.movimientos:
                self._vista.overlay.ui.cmb_presupuesto_meta.setCurrentIndex(cantidad_presupuestos + i)
                return

    def set_modelo_transacciones(self, modelo):
        self._modelo_transacciones = modelo

    @staticmethod
    def llenar_combo(lista: list,  # Ahora recibimos (index, enum_member)
                     combobox: QComboBox):
        for index, item in enumerate(lista):
            combobox.addItem(item, index)

    def verificar_monto(self):
        txt_monto: QLineEdit = self.sender()
        monto = txt_monto.text()
        print(monto)
        if monto == "":
            txt_monto.setStyleSheet("")
            self.monto_valido = False
        elif not self._validar_decimal(monto):
            print("El valor ingresado no es correcto") # Para depuración
            txt_monto.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.monto_valido = False
        elif Decimal(monto) <= 0:
            print("El monto no puede ser negativo") # Para depuración
            txt_monto.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.monto_valido = False
        else:
            txt_monto.setStyleSheet("")
            self.monto_valido = True

    @staticmethod
    def _validar_decimal(texto: str) -> bool:
        try:
            Decimal(texto)
            return True
        except InvalidOperation:
            return False

    @staticmethod
    def verificar_combo(combobox):
        if combobox.currentIndex() == -1:
            combobox.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            print("Debe seleccionar al menos una opción")
            return False
        else:
            combobox.setStyleSheet("")
            return True

    def guardar_transaccion(self):
        if not self.descripcion_valida:
            return
        if not self.monto_valido:
            return
        if not self.presupuesto_meta_valido:
            return
        if not self.categoria_valido:
            return
        if not self.tipo_movimiento_valido:
            return

        descripcion = self._vista.overlay.ui.txt_descripcion_transaccion.text()
        # Obtener el texto del monto de forma más segura
        monto_widget = self._vista.overlay.ui.txt_monto_transaccion
        monto_texto_original = monto_widget.text()

        print(f'Texto del monto original: "{monto_texto_original}"')
        print(f'Longitud del texto: {len(monto_texto_original)}')
        print(f'Representación bytes: {monto_texto_original.encode("utf-8")}')
        monto = Decimal(monto_texto_original)
        fecha = self._vista.overlay.ui.fch_transaccion.date().toPyDate()
        indice_tipo_movimiento = self._vista.overlay.ui.cmb_tipo_transaccion.currentIndex()
        tipo_movimiento = TiposTransaccion.INGRESO
        notas = self._vista.overlay.ui.ptxt_notas_adicionales.toPlainText()

        if self.modo_edicion and self.movimiento_editando:
            # Actualizar movimiento existente
            self._actualizar_movimiento_existente(descripcion, monto, fecha, indice_tipo_movimiento, notas)
        else:
            # Crear nuevo movimiento
            self._crear_nuevo_movimiento(descripcion, monto, fecha, indice_tipo_movimiento, tipo_movimiento, notas)

        ManejadorArchivos.guardar_archivo(self._usuario.id, self._usuario)
        QMessageBox.information(
            self._vista.overlay,
            "Registro exitoso",
            "El movimiento se guardó exitosamente"
        )
        self._vista.ocultar_modal(False)
        self.cargar_transacciones_en_tabla()

    def _actualizar_movimiento_existente(self, descripcion, monto, fecha, indice_tipo_movimiento, notas):
        """Actualiza un movimiento existente"""
        movimiento = self.movimiento_editando

        # Remover de presupuestos/metas anteriores si es necesario
        self._remover_de_presupuestos_metas(movimiento)

        # Actualizar datos del movimiento
        movimiento.descripcion = descripcion
        movimiento.monto = monto
        movimiento.fecha_transaccion = fecha
        movimiento.notas = notas
        movimiento.categoria = None  # Reset categoría

        # Configurar tipo y asociaciones
        if indice_tipo_movimiento == 0:
            movimiento.tipo_movimiento = TiposTransaccion.INGRESO
        else:
            movimiento.tipo_movimiento = TiposTransaccion.EGRESO
            self._asociar_a_presupuesto_meta(movimiento)

    def _crear_nuevo_movimiento(self, descripcion, monto, fecha, indice_tipo_movimiento, tipo_movimiento, notas):
        """Crea un nuevo movimiento"""
        nuevo_movimiento = Movimiento(
            descripcion=descripcion,
            monto=monto,
            fecha_transaccion=fecha,
            tipo_movimiento=tipo_movimiento,
            notas=notas
        )

        if indice_tipo_movimiento == 1:
            nuevo_movimiento.tipo_movimiento = TiposTransaccion.EGRESO
            self._asociar_a_presupuesto_meta(nuevo_movimiento)

        self._usuario.agregar_movimiento(nuevo_movimiento)

    def _remover_de_presupuestos_metas(self, movimiento: Movimiento):
        """Remueve el movimiento de presupuestos y metas"""
        # Remover de presupuestos
        for presupuesto in self._usuario.presupuestos:
            if movimiento.id in presupuesto.movimientos:
                presupuesto.movimientos.remove(movimiento.id)

        # Remover de metas
        for meta in self._usuario.metas:
            if movimiento.id in meta.movimientos:
                meta.movimientos.remove(movimiento.id)

    def _asociar_a_presupuesto_meta(self, movimiento: Movimiento):
        """Asocia el movimiento a un presupuesto o meta"""
        cantidad_presupuestos = len(self._usuario.presupuestos)
        indice_presupuesto_meta = self._vista.overlay.ui.cmb_presupuesto_meta.currentIndex()

        if indice_presupuesto_meta < cantidad_presupuestos:
            presupuesto = self._usuario.presupuestos[indice_presupuesto_meta]
            indice_categoria = self._vista.overlay.ui.cmb_categoria_transaccion.currentData()
            categoria = list(presupuesto.categorias.keys())[indice_categoria]
            movimiento.categoria = categoria
            presupuesto.categorias[categoria] = True
            presupuesto.agregar_egreso(movimiento.id)
        else:
            meta = self._usuario.metas[indice_presupuesto_meta - cantidad_presupuestos]
            meta.agregar_egreso(movimiento.id)

    def actualizar_banderas(self, valor: bool = False):
        self.tipo_movimiento_valido = valor
        self.presupuesto_meta_valido = valor
        self.categoria_valido = valor
        self.monto_valido = valor
        self.descripcion_valida = valor

    def inicializar_tabla_transacciones(self):
        """Inicializa la tabla de transacciones con headers y configuración"""
        # Crear el modelo
        self.modelo_tabla = QStandardItemModel()

        # Definir las columnas
        headers = ["Fecha", "Descripción", "Tipo", "Categoría", "Monto", "Notas"]
        self.modelo_tabla.setHorizontalHeaderLabels(headers)

        # Asignar el modelo a la tabla
        self._vista.ui.lst_transacciones.setModel(self.modelo_tabla)

        # Configurar el ancho de las columnas
        self._configurar_tabla()

        # Conectar evento de doble clic
        self._vista.ui.lst_transacciones.doubleClicked.connect(self._detectar_doble_click)

        # Cargar todas las transacciones inicialmente
        self.cargar_transacciones_en_tabla()

    def _configurar_tabla(self):
        """Configura la apariencia y comportamiento de la tabla"""
        tabla = self._vista.ui.lst_transacciones

        # Configurar ancho de columnas
        tabla.setColumnWidth(0, 100)  # Fecha
        tabla.setColumnWidth(1, 500)  # Descripción
        tabla.setColumnWidth(2, 80)   # Tipo
        tabla.setColumnWidth(3, 120)  # Categoría
        tabla.setColumnWidth(4, 100)  # Monto
        tabla.setColumnWidth(5, 100)  # Notas

        # Configurar selección
        tabla.setSelectionBehavior(tabla.SelectionBehavior.SelectRows)
        tabla.setAlternatingRowColors(True)

        # Hacer que las columnas se ajusten al contenido
        tabla.horizontalHeader().setStretchLastSection(True)

        # Habilitar ordenamiento por columnas
        tabla.setSortingEnabled(True)

        # Configurar headers para permitir ordenamiento
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

    def _detectar_doble_click(self, index):
        """Maneja el doble click en una fila de la tabla"""
        if not index.isValid():
            return

        movimiento = self.obtener_transaccion_seleccionada()
        if movimiento:
            self.mostrar_modal_edicion(movimiento)

    def cargar_transacciones_en_tabla(self, movimientos_filtrados=None):
        """Carga las transacciones en la tabla"""
        if movimientos_filtrados is None:
            movimientos_filtrados = self._usuario.movimientos

        # Limpiar la tabla
        self.modelo_tabla.clear()

        # Reestablecer headers después de limpiar
        headers = ["Fecha", "Descripción", "Tipo", "Categoría", "Monto", "Notas"]
        self.modelo_tabla.setHorizontalHeaderLabels(headers)

        # Ordenar movimientos por fecha (más recientes primero)
        movimientos_ordenados = sorted(movimientos_filtrados,
                                       key=lambda m: m.fecha_transaccion,
                                       reverse=True)

        # Agregar cada movimiento como una fila
        for movimiento in movimientos_ordenados:
            self._agregar_fila_movimiento(movimiento)

        print(f"Cargadas {len(movimientos_ordenados)} transacciones en la tabla.")

    def _agregar_fila_movimiento(self, movimiento: Movimiento):
        """Agrega una fila con los datos del movimiento a la tabla"""
        fila = []

        # Fecha - hacer que no sea editable
        fecha_item = QStandardItem(movimiento.fecha_transaccion.strftime("%d/%m/%Y"))
        fecha_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        fecha_item.setEditable(False)  # No editable
        fila.append(fecha_item)

        # Descripción - hacer que no sea editable
        descripcion_item = QStandardItem(movimiento.descripcion)
        descripcion_item.setEditable(False)  # No editable
        fila.append(descripcion_item)

        # Tipo - hacer que no sea editable
        tipo_texto = "Ingreso" if movimiento.tipo_movimiento.value.nombre == "Ingreso" else "Egreso"
        tipo_item = QStandardItem(tipo_texto)
        tipo_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        tipo_item.setEditable(False)  # No editable

        # Colorear según el tipo
        if tipo_texto == "Ingreso":
            tipo_item.setForeground(Qt.GlobalColor.darkGreen)
        else:
            tipo_item.setForeground(Qt.GlobalColor.darkRed)

        fila.append(tipo_item)

        # Categoría - hacer que no sea editable
        categoria_item = QStandardItem(movimiento.categoria if movimiento.categoria else "Sin categoría")
        categoria_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        categoria_item.setEditable(False)  # No editable
        fila.append(categoria_item)

        # Monto - hacer que no sea editable
        monto_texto = f"${movimiento.monto:,.2f}"
        monto_item = QStandardItem(monto_texto)
        monto_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        monto_item.setEditable(False)  # No editable

        # Colorear el monto según el tipo
        if tipo_texto == "Ingreso":
            monto_item.setForeground(Qt.GlobalColor.darkGreen)
        else:
            monto_item.setForeground(Qt.GlobalColor.darkRed)

        fila.append(monto_item)

        # Notas - hacer que no sea editable
        notas_item = QStandardItem(movimiento.notas if movimiento.notas else "")
        notas_item.setEditable(False)  # No editable
        fila.append(notas_item)

        # Agregar la fila al modelo
        self.modelo_tabla.appendRow(fila)

    def inicializar_filtros(self):
        """Inicializa los filtros y conecta los eventos de los botones de búsqueda"""
        # Inicializar la tabla primero
        self.inicializar_tabla_transacciones()

        # Llenar combo de tipos para filtros
        self.llenar_combo(["Todos"] + list(map(lambda t: t.value.nombre, TiposTransaccion)),
                          self._vista.ui.cmb_tipo_transaccion)

        # Llenar combo de presupuestos/metas para filtros
        self._actualizar_combo_presupuesto_filtro()

        # Conectar eventos de filtros
        self._vista.ui.btn_buscar_transacciones.clicked.connect(self.aplicar_filtros)
        self._vista.ui.btn_limpiar_filtros.clicked.connect(self.limpiar_filtros)
        self._vista.ui.cmb_presupuesto.currentIndexChanged.connect(self._actualizar_combo_categoria_filtro)

    def _actualizar_combo_presupuesto_filtro(self):
        """Actualiza el combo de presupuestos/metas para filtros"""
        cmb_presupuesto = self._vista.ui.cmb_presupuesto
        cmb_presupuesto.clear()

        # Agregar opción "Todos"
        cmb_presupuesto.addItem("Todos", -1)

        # Agregar presupuestos activos
        presupuestos_activos = [p for p in self._usuario.presupuestos if p.esta_activo]
        for i, presupuesto in enumerate(presupuestos_activos):
            cmb_presupuesto.addItem(f"Presupuesto: {presupuesto.nombre}", f"presupuesto_{i}")

        # Agregar metas activas
        metas_activas = [m for m in self._usuario.metas if m.esta_activo]
        for i, meta in enumerate(metas_activas):
            cmb_presupuesto.addItem(f"Meta: {meta.nombre}", f"meta_{i}")

    def _actualizar_combo_categoria_filtro(self):
        """Actualiza el combo de categorías basado en el presupuesto seleccionado"""
        cmb_categoria = self._vista.ui.cmb_categoria_transaccion
        cmb_presupuesto = self._vista.ui.cmb_presupuesto

        cmb_categoria.clear()
        cmb_categoria.addItem("Todas", -1)

        if cmb_presupuesto.currentIndex() == 0:  # "Todos" seleccionado
            # Agregar todas las categorías de todos los presupuestos
            todas_categorias = set()
            for presupuesto in self._usuario.presupuestos:
                if presupuesto.esta_activo:
                    todas_categorias.update(presupuesto.categorias.keys())

            for categoria in sorted(todas_categorias):
                cmb_categoria.addItem(categoria, categoria)
        else:
            # Obtener categorías del presupuesto específico
            data = cmb_presupuesto.currentData()
            if data and isinstance(data, str) and data.startswith("presupuesto_"):
                indice = int(data.split("_")[1])
                presupuestos_activos = [p for p in self._usuario.presupuestos if p.esta_activo]
                if indice < len(presupuestos_activos):
                    presupuesto = presupuestos_activos[indice]
                    for categoria in presupuesto.categorias.keys():
                        cmb_categoria.addItem(categoria, categoria)

    def aplicar_filtros(self):
        """Aplica los filtros seleccionados y actualiza la lista de transacciones"""
        movimientos_filtrados = self._filtrar_movimientos()
        self.cargar_transacciones_en_tabla(movimientos_filtrados)
        print(f"Filtros aplicados. Mostrando {len(movimientos_filtrados)} transacciones.")

    def _filtrar_movimientos(self) -> List[Movimiento]:
        """Filtra los movimientos según los criterios seleccionados"""
        movimientos_filtrados = self._usuario.movimientos.copy()

        # Filtrar por tipo de transacción
        tipo_seleccionado = self._vista.ui.cmb_tipo_transaccion.currentIndex()
        if tipo_seleccionado > 0:  # No es "Todos"
            tipo_movimiento = list(TiposTransaccion)[tipo_seleccionado - 1]
            movimientos_filtrados = [m for m in movimientos_filtrados
                                     if m.tipo_movimiento == tipo_movimiento]

        # Filtrar por presupuesto/meta
        presupuesto_data = self._vista.ui.cmb_presupuesto.currentData()
        if presupuesto_data != -1 and presupuesto_data:  # No es "Todos"
            if isinstance(presupuesto_data, str):
                if presupuesto_data.startswith("presupuesto_"):
                    # Filtrar por presupuesto específico
                    indice = int(presupuesto_data.split("_")[1])
                    presupuestos_activos = [p for p in self._usuario.presupuestos if p.esta_activo]
                    if indice < len(presupuestos_activos):
                        presupuesto_seleccionado = presupuestos_activos[indice]
                        movimientos_filtrados = self._filtrar_por_presupuesto(
                            movimientos_filtrados, presupuesto_seleccionado)

                elif presupuesto_data.startswith("meta_"):
                    # Filtrar por meta específica
                    indice = int(presupuesto_data.split("_")[1])
                    metas_activas = [m for m in self._usuario.metas if m.esta_activo]
                    if indice < len(metas_activas):
                        meta_seleccionada = metas_activas[indice]
                        movimientos_filtrados = self._filtrar_por_meta(
                            movimientos_filtrados, meta_seleccionada)

        # Filtrar por categoría
        categoria_data = self._vista.ui.cmb_categoria_transaccion.currentData()
        if categoria_data != -1 and categoria_data:  # No es "Todas"
            movimientos_filtrados = [m for m in movimientos_filtrados
                                     if m.categoria == categoria_data]

        return movimientos_filtrados

    @staticmethod
    def _filtrar_por_presupuesto(movimientos: List[Movimiento], presupuesto) -> List[Movimiento]:
        """Filtra movimientos que pertenecen a un presupuesto específico"""
        return [m for m in movimientos
                if (m.id in presupuesto.movimientos or  # Movimiento asociado al presupuesto
                    (m.categoria in presupuesto.categorias.keys() if m.categoria else False)) and
                presupuesto.inicio_presupuesto <= m.fecha_transaccion <= presupuesto.fin_presupuesto]

    @staticmethod
    def _filtrar_por_meta(movimientos: List[Movimiento], meta) -> List[Movimiento]:
        """Filtra movimientos que pertenecen a una meta específica"""
        return [m for m in movimientos
                if m.id in meta.movimientos and  # Movimiento asociado a la meta
                meta.fecha_inicio <= m.fecha_transaccion <= meta.fecha_limite]

    def limpiar_filtros(self):
        """Limpia todos los filtros y muestra todas las transacciones"""
        # Resetear combos a "Todos"
        self._vista.ui.cmb_tipo_transaccion.setCurrentIndex(0)
        self._vista.ui.cmb_presupuesto.setCurrentIndex(0)
        self._vista.ui.cmb_categoria_transaccion.setCurrentIndex(0)

        # Cargar todas las transacciones
        self.cargar_transacciones_en_tabla()
        print("Filtros limpiados. Mostrando todas las transacciones.")

    def obtener_transaccion_seleccionada(self) -> Movimiento | None:
        """Obtiene la transacción seleccionada en la tabla"""
        tabla = self._vista.ui.lst_transacciones
        indices_seleccionados = tabla.selectionModel().selectedRows()

        if not indices_seleccionados:
            return None

        # Obtener la fila seleccionada
        fila = indices_seleccionados[0].row()
        print(f"Fila seleccionada: {fila}")

        # Obtener los datos de la fila para buscar el movimiento
        descripcion_item = self.modelo_tabla.item(fila, 1)  # Columna descripción
        fecha_item = self.modelo_tabla.item(fila, 0)  # Columna fecha
        monto_item = self.modelo_tabla.item(fila, 4)  # Columna monto
        tipo_item = self.modelo_tabla.item(fila, 2)  # Columna tipo

        if not all([descripcion_item, fecha_item, monto_item, tipo_item]):
            print("No se pudieron obtener todos los datos de la fila")
            return None

        descripcion = descripcion_item.text()
        fecha_str = fecha_item.text()
        monto_str = monto_item.text().replace("$", "").replace(",", "")
        tipo_str = tipo_item.text()


        # Convertir fecha de string a date para comparación
        try:
            from datetime import datetime
            fecha_buscada = datetime.strptime(fecha_str, "%d/%m/%Y").date()
        except ValueError as e:
            print(f"Error al parsear fecha: {e}")
            return None

        # Convertir monto a Decimal para comparación
        try:
            monto_buscado = Decimal(monto_str)
        except (InvalidOperation, ValueError) as e:
            print(f"Error al parsear monto: {e}")
            return None

        # Determinar tipo de movimiento
        tipo_buscado = TiposTransaccion.INGRESO if tipo_str == "Ingreso" else TiposTransaccion.EGRESO

        # Buscar el movimiento correspondiente usando múltiples criterios
        movimientos_candidatos = []

        for movimiento in self._usuario.movimientos:
            # Comparar todos los criterios
            if (movimiento.descripcion == descripcion and
                    movimiento.fecha_transaccion == fecha_buscada and
                    movimiento.tipo_movimiento == tipo_buscado):

                # Comparar montos con tolerancia para evitar problemas de precisión
                if self._montos_son_iguales(movimiento.monto, monto_buscado):
                    movimientos_candidatos.append(movimiento)

        # Si encontramos exactamente uno, lo retornamos
        if len(movimientos_candidatos) == 1:
            print(f"Movimiento encontrado: {movimientos_candidatos[0].id}")
            return movimientos_candidatos[0]
        elif len(movimientos_candidatos) > 1:
            print(f"Se encontraron {len(movimientos_candidatos)} movimientos candidatos")
            # Si hay múltiples candidatos, usar el primero (podrías implementar lógica adicional aquí)
            return movimientos_candidatos[0]
        else:
            print("No se encontró ningún movimiento que coincida")
            # Debug adicional
            print("Movimientos disponibles:")
            for i, mov in enumerate(self._usuario.movimientos):
                print(f"  {i}: {mov.descripcion} - {mov.fecha_transaccion} - {mov.monto} - {mov.tipo_movimiento.value.nombre}")
            return None

    @staticmethod
    def _montos_son_iguales(monto1: Decimal, monto2: Decimal, tolerancia: Decimal = Decimal('0.01')) -> bool:
        """Compara dos montos con una tolerancia para evitar problemas de precisión"""
        return abs(monto1 - monto2) < tolerancia