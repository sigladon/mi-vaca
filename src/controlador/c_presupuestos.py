import copy
import re
from datetime import date
from decimal import Decimal, InvalidOperation

from PyQt6.QtCore import QObject, QDate, Qt
from PyQt6.QtWidgets import QLineEdit, QDateEdit, QWidget, QHBoxLayout, QLabel, QPushButton, QMessageBox, QVBoxLayout

from src.modelo.entidades.presupuesto import Presupuesto
from src.modelo.entidades.usuario import Usuario
from src.utils.manejador_archivos import ManejadorArchivos
from src.vista.overlay_presupuesto import OverlayPresupuesto
from src.vista.panel_presupuestos import PanelPresupuesto


class CPresupuestos(QObject):
    def __init__(self, vista: PanelPresupuesto, usuario: Usuario):
        super().__init__()
        self.nombre_valido = None
        self._index_presupuesto_editar = None
        self.fecha_fin_valido = True
        self.fecha_inicio_valido = True
        self.limite_valido = False
        self._vista = vista
        self._usuario = usuario
        self._id_presupuesto = ""
        self._categorias_base = {
            "Vivienda": False,
            "Alimentación": False,
            "Transporte": False,
            "Deudas": False,
            "Obligaciones Tributarias": False,
            "Salud": False,
            "Cuidado Personal": False,
            "Ahorro": False,
            "Ocio y Entretenimiento": False,
        }
        self._categorias_agregadas = copy.deepcopy(self._categorias_base)

        self.actualizar_contadores_presupuestos()

        self._vista.overlay = OverlayPresupuesto(self._vista)
        self._vista.overlay.ui.txt_nombre_presupuesto.editingFinished.connect(self.verificar_nombre)
        self._vista.overlay.ui.txt_limite_presupuesto.editingFinished.connect(self.verificar_limite)
        self._vista.overlay.ui.fch_fecha_inicio.editingFinished.connect(self.verificar_fecha_inicio)
        self._vista.overlay.ui.fch_fecha_fin.editingFinished.connect(self.verificar_fecha_fin)
        self._vista.overlay.ui.btn_agregar_categoria.clicked.connect(self.agregar_categoria)
        self._vista.ui.btn_agregar_presupuesto.clicked.connect(self.mostrar_modal)
        self._vista.overlay.ui.btn_crear_presupuesto.clicked.connect(self.guardar_presupuesto)
        self.actualizar_vista_presupuestos()

    def mostrar_modal(self):
        self._categorias_agregadas = copy.deepcopy(self._categorias_base)
        self._actualizar_banderas()
        self._limpiar_vista_presupuesto()
        self.actualizar_vista_categorias()
        self._index_presupuesto_editar = None
        self._vista.overlay.ui.btn_borrar_presupuesto.hide()
        self._vista.mostrar_modal()

    def verificar_nombre(self):
        txt_nombre: QLineEdit = self.sender()
        nombre = txt_nombre.text()
        if nombre == "":
            txt_nombre.setStyleSheet("")
            self.nombre_valido = False
        elif not self._validar_nombre(nombre):
            print("El nombre del presupuesto no es válido") # Para depuración
            txt_nombre.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.nombre_valido = False
        else:
            txt_nombre.setStyleSheet("")
            self.nombre_valido = True

    def verificar_limite(self):
        txt_limite: QLineEdit = self.sender()
        limite = txt_limite.text()
        if limite == "":
            txt_limite.setStyleSheet("")
            self.limite_valido = False
        elif not self._validar_decimal(limite):
            print("El valor ingresado no es correcto") # Para depuración
            txt_limite.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.limite_valido = False
        elif Decimal(limite) <= 0:
            print("El valor límite no puede ser negativo") # Para depuración
            txt_limite.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.limite_valido = False
        else:
            txt_limite.setStyleSheet("")
            self.limite_valido = True

    def verificar_fecha_inicio(self):
        fch_fecha_inicio: QDateEdit = self.sender()
        fecha_inicio = fch_fecha_inicio.date().toPyDate()
        inicio_mes_actual = date.today().replace(day=1)
        if fecha_inicio >= inicio_mes_actual:
            fch_fecha_inicio.setStyleSheet("")
            self.fecha_inicio_valido = True
        else:
            print("El valor límite no puede ser negativo") # Para depuración
            fch_fecha_inicio.setStyleSheet("border: 1px solid red; ")
            self.fecha_inicio_valido = False

    def verificar_fecha_fin(self):
        fch_fecha_fin: QDateEdit = self.sender()
        fecha_fin = fch_fecha_fin.date().toPyDate()
        fecha_inicio = self._vista.overlay.ui.fch_fecha_inicio.date().toPyDate()
        if fecha_fin > fecha_inicio:
            fch_fecha_fin.setStyleSheet("")
            self.fecha_fin_valido = True
        else:
            print("El valor límite no puede ser negativo") # Para depuración
            fch_fecha_fin.setStyleSheet("border: 1px solid red; ")
            self.fecha_fin_valido = False

    def agregar_categoria(self):
        txt_nombre_categoria: QLineEdit = self._vista.overlay.ui.txt_nombre_categoria
        nombre_categoria = txt_nombre_categoria.text()
        if not nombre_categoria:
            print("El nombre de la categoría no puede estar vacío")
            return

        if not self._validar_nombre(nombre_categoria):
            print("El nombre de la categoría no es válido") # Para depuración
            return

        if nombre_categoria in self._categorias_agregadas.keys():
            print("Esa categoría ya está agregada") # Para depuración
            return

        print("Agregando categoría") # Para depuración
        self._categorias_agregadas[nombre_categoria] = False
        self.actualizar_vista_categorias()

    def guardar_presupuesto(self):
        if not self.verificar_numero_categorias():
            QMessageBox.warning(
                self._vista.overlay,
                "Error",
                f"Debes agregar al menos 2 categorías"
            )
            return

        if not (self.nombre_valido and self.limite_valido and self.fecha_inicio_valido and self.fecha_fin_valido):
            QMessageBox.warning(
                self._vista.overlay,
                "Error",
                f"Existen datos incorrectos"
            )
            return

        aux = Decimal('0.01')
        nombre = self._vista.overlay.ui.txt_nombre_presupuesto.text()
        limite = Decimal(self._vista.overlay.ui.txt_limite_presupuesto.text()).quantize(aux)
        fecha_inicio = self._vista.overlay.ui.fch_fecha_inicio.date().toPyDate()
        fecha_fin = self._vista.overlay.ui.fch_fecha_fin.date().toPyDate()
        categorias = copy.deepcopy(self._categorias_agregadas)
        recibir_notificacion = self._vista.overlay.ui.cbx_recibir_notificaciones.isChecked()
        notas = self._vista.overlay.ui.ptxt_notas.toPlainText()

        if self._index_presupuesto_editar is None:
            nuevo_presupuesto = Presupuesto(
                nombre=nombre,
                limite=limite,
                inicio_presupuesto=fecha_inicio,
                fin_presupuesto=fecha_fin,
                categorias=categorias,
                notas=notas,
                notificar_usuario=recibir_notificacion,
            )
            self._usuario.agregar_presupuesto(nuevo_presupuesto)
        else:
            presupuesto_editado = self._usuario.presupuestos[self._index_presupuesto_editar]
            presupuesto_editado.nombre = nombre
            presupuesto_editado.limite = limite
            presupuesto_editado.inicio_presupuesto = fecha_inicio
            presupuesto_editado.fin_presupuesto = fecha_fin
            presupuesto_editado.categorias = categorias
            presupuesto_editado.notas = notas
            presupuesto_editado.notificar_usuario=recibir_notificacion

        print(self._usuario.presupuestos)

        ManejadorArchivos.guardar_archivo(self._usuario.id, self._usuario)

        QMessageBox.information(
            self._vista.overlay,
            "Registro exitóso",
            "El presupuesto se guardó existosamente"
        )

        self.actualizar_vista_presupuestos()
        self.actualizar_contadores_presupuestos()
        self._vista.ocultar_modal(False)



    def verificar_numero_categorias(self):
        return len(self._categorias_agregadas) > 1

    def actualizar_contadores_presupuestos(self):
        self._vista.ui.lbl_limite_total.setText(f"$ {str(self._calcular_limite_total())}")
        self._vista.ui.lbl_total_presupuestos.setText(str(self._calcular_cantidad_presupuestos()))
        self._vista.ui.lbl_presupuestos_activos.setText(str(self._calcular_presupuestos_activos()))

    def _calcular_cantidad_presupuestos(self):
        return len(self._usuario.presupuestos)

    def _calcular_presupuestos_activos(self):
        return len(list(filter(lambda p: p.esta_activo, self._usuario.presupuestos)))

    def _calcular_limite_total(self):
        aux = Decimal('0.01')
        return sum(presupuesto.limite.quantize(aux) for presupuesto in self._usuario.presupuestos)

    def _crear_widget_categoria(self, categoria):
        widget_categoria = QWidget()
        widget_categoria.setObjectName(f"categoria_{categoria}")
        widget_categoria.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 4px;
                margin: 2px 0px;
            }
            QWidget:hover {
                background-color: #e9ecef;
            }
        """)

        layout = QHBoxLayout(widget_categoria)
        layout.setContentsMargins(12,8,12,8)
        layout.setSpacing(10)

        lbl_nombre = QLabel(categoria)
        lbl_nombre.setStyleSheet("""
        QLabel {
            font-weight: 500;
            color: #343a40;
            background: transparent;
            border: none;
            font-size: 14px;
        }
        """)
        layout.addWidget(lbl_nombre)
        layout.addStretch()

        btn_eliminar: QPushButton = QPushButton("x")
        btn_eliminar.setFixedSize(32,32)
        btn_eliminar.setStyleSheet("""
        QPushButton {
            padding: 0;
            background-color: #dc3545;
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: bold;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #c82333;
        }
        QPushButton:pressed {
            background-color: #bd2130;
        }
        QPushButton:disabled {
            background-color: #6c757d;
            color: #adb5bd;
        }
        """)

        puede_eliminar = self._categorias_agregadas.get(categoria, False) == False
        btn_eliminar.setEnabled(puede_eliminar)

        if puede_eliminar:
            btn_eliminar.setToolTip("Eliminar categoría")
            btn_eliminar.clicked.connect(lambda: self.eliminar_categoria(categoria))
        else:
            btn_eliminar.setToolTip("Esta categoría no se puede eliminar")

        layout.addWidget(btn_eliminar)

        return widget_categoria

    def actualizar_vista_categorias(self):
        self._vista.overlay.ui.txt_nombre_categoria.clear()
        layout = self._vista.overlay.ui.contenedor_categoria.layout()

        if layout is None:
            layout = QVBoxLayout(self._vista.overlay.ui.contenedor_categoria)
            layout.setObjectName("verticalLayout")

        while layout.count():
            item = layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    item.widget().setParent(None)
                    item.widget().deleteLater()

        for categoria in self._categorias_agregadas.keys():
            widget_categoria = self._crear_widget_categoria(categoria)
            layout.addWidget(widget_categoria)

        layout.addStretch()

        self._vista.overlay.ui.contenedor_categoria.updateGeometry()

    def eliminar_categoria(self, categoria):
        if categoria not in self._categorias_agregadas:
            print(f"Error: La categoría {categoria} no existe")
            return

        if self._categorias_agregadas[categoria]:
            print(f"Error: La categoría {categoria} no se puede borrar")
            QMessageBox.warning(
                self._vista.overlay,
                "Advertencia",
                f"La categoría {categoria} no se puede eliminar"
            )
            return

        respuesta = QMessageBox.question(
            self._vista.overlay,
            "Confirmar eliminación",
            f"̉¿Estás seguro de que quieres eliminar la categoría {categoria}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            del self._categorias_agregadas[categoria]
            self.actualizar_vista_categorias()

    @staticmethod
    def _validar_nombre(nombre):
        regex_nombre = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ' ]{2,50}$")
        return regex_nombre.match(nombre)

    @staticmethod
    def _validar_decimal(texto: str) -> bool:
        try:
            Decimal(texto)
            return True
        except InvalidOperation:
            return False

    def actualizar_vista_presupuestos(self):
        container_widget = self._vista.ui.contenedor_presupuestos.widget()

        if container_widget is None:
            return

        layout = container_widget.layout()

        if layout is None:
            layout = QVBoxLayout(container_widget)
            layout.setObjectName("verticalLayout_5")
            layout.setContentsMargins(10,10,10,10)
            layout.setSpacing(8)

        self._limpiar_layout(layout)

        if not self._usuario.presupuestos:
            lbl_vacio = QLabel("No tienes presupuestos aún. Prueba creando uno.")
            lbl_vacio.setStyleSheet("""
                QLabel {
                    padding: 0;
                    color: #6c757d;
                    font-size: 14px;
                    font-style: italic;
                    padding: 20px;
                    text-align: center;
                    background: transparent;
                    border: none;
                }
            """)
            lbl_vacio.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(lbl_vacio)
        else:
            for index, presupuesto in enumerate(self._usuario.presupuestos):
                widget_presupuesto = self._crear_widget_presupuesto(index,presupuesto)
                layout.addWidget(widget_presupuesto)

        layout.addStretch()

        container_widget.updateGeometry()
        container_widget.update()

    @staticmethod
    def _limpiar_layout(layout):
        """Limpia todos los widgets de un layout correctamente"""
        while layout.count():
            item = layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    # CORRECCIÓN: Desconectar señales antes de eliminar
                    try:
                        widget.setParent(None)
                        # widget.disconnect()  # Desconectar todas las señales
                    except TypeError:
                        pass  # Ignorar errores de desconexión
                    finally:
                        widget.deleteLater()

    def _crear_widget_presupuesto(self, index, presupuesto):
        widget_presupuesto = QWidget()
        widget_presupuesto.setObjectName(f"presupuesto_{presupuesto.id}")
        widget_presupuesto.setFixedHeight(160)
        widget_presupuesto.setStyleSheet("""
        QWidget {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 12px;
            margin: 4px 0px;
        }
        QWidget:hover {
            background-color: #f8f9fa;
            border-color: #007bff;
        }
        """)

        layout_principal = QHBoxLayout(widget_presupuesto)
        layout_principal.setContentsMargins(24,8,24,8)
        layout_principal.setSpacing(4)

        layout_info = QVBoxLayout()
        layout_info.setSpacing(4)

        layout_nombre = QHBoxLayout()
        layout_nombre.setSpacing(10)

        lbl_nombre = QLabel(presupuesto.nombre)
        lbl_nombre.setStyleSheet("""
        QLabel {
            font-weight: bold;
            font-size: 16px;
            color: #2c3e50;
            background: transparent;
            border: none;
            padding: 0;
        }
        """)
        layout_nombre.addWidget(lbl_nombre)

        lbl_estado = QLabel("ACTIVO" if presupuesto.esta_activo else "INACTIVO")
        estado_color = "#28a745" if presupuesto.esta_activo else "#6c757d"
        lbl_estado.setStyleSheet(f"""
            QLabel {{
                background-color: {estado_color};
                color: white;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: bold;
                border: none;
                padding: 0;
            }}
        """)

        lbl_estado.setFixedHeight(24)
        layout_nombre.addWidget(lbl_estado)
        layout_nombre.addStretch()

        layout_info.addLayout(layout_nombre)

        movimientos_presupuesto = self._usuario.movimientos
        monto_gastado = presupuesto.obtener_monto_gastado(list(filter(lambda m: m.id_vinculado == presupuesto.id, movimientos_presupuesto)))
        porcentaje = presupuesto.obtener_porcentaje(movimientos_presupuesto)

        aux = Decimal("0.01")
        lbl_limite = QLabel(f"Limite: ${presupuesto.limite.quantize(aux)}")
        lbl_limite.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #495057;
                background: transparent;
                border: none;
                padding: 0;
            }
        """)
        layout_info.addWidget(lbl_limite)

        lbl_gastado = QLabel(f"Gastado: ${monto_gastado:,.2f}")
        color_gastado = "#dc3545" if porcentaje >= 100 else "#28a745" if porcentaje < 80 else "#ffc107"
        lbl_gastado.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                color: {color_gastado};
                font-weight: 500;
                background: transparent;
                border: none;
                padding: 0;
            }}
        """)
        layout_info.addWidget(lbl_gastado)

        # Barra de progreso personalizada
        widget_progreso = self._crear_barra_progreso(porcentaje)
        layout_info.addWidget(widget_progreso)

        # Etiqueta de porcentaje
        lbl_porcentaje = QLabel(f"{porcentaje:.1f}%")
        lbl_porcentaje.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: bold;
                color: {color_gastado};
                background: transparent;
                border: none;
                padding: 0;
            }}
        """)
        layout_info.addWidget(lbl_porcentaje)

        layout_principal.addLayout(layout_info)

        # Spacer para empujar el botón a la derecha
        layout_principal.addStretch()

        # Botón de editar
        btn_editar: QPushButton = QPushButton("Editar")
        btn_editar.setFixedSize(80, 35)
        btn_editar.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 500;
                font-size: 13px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        btn_editar.clicked.connect(lambda: self.editar_presupuesto(index,presupuesto))
        layout_principal.addWidget(btn_editar)

        return widget_presupuesto

    @staticmethod
    def _crear_barra_progreso(porcentaje):
        """Crea una barra de progreso personalizada"""
        widget_barra = QWidget()
        widget_barra.setFixedHeight(8)
        widget_barra.setStyleSheet("""
            QWidget {
                background-color: #e9ecef;
                border-radius: 4px;
                border: none;
            }
        """)

        # Crear el widget de progreso interno
        widget_progreso = QWidget(widget_barra)

        # Determinar color según el porcentaje
        if porcentaje >= 100:
            color_progreso = "#dc3545"  # Rojo - excedido
        elif porcentaje >= 80:
            color_progreso = "#ffc107"  # Amarillo - advertencia
        else:
            color_progreso = "#28a745"  # Verde - normal

        widget_progreso.setStyleSheet(f"""
            QWidget {{
                background-color: {color_progreso};
                border-radius: 4px;
                border: none;
            }}
        """)

        # Calcular el ancho del progreso (máximo 100%)
        ancho_porcentaje = min(porcentaje, 100)

        # El ancho se calculará dinámicamente cuando se muestre el widget
        def actualizar_progreso():
            ancho_total = widget_barra.width()
            ancho_progreso = int((ancho_total * ancho_porcentaje) / 100)
            widget_progreso.setGeometry(0, 0, ancho_progreso, 8)

        # Conectar evento de redimensionado
        widget_barra.resizeEvent = lambda event: actualizar_progreso()

        return widget_barra

    def editar_presupuesto(self, index, presupuesto):
        """Abre el modal para editar un presupuesto existente"""
        print(f"Editando presupuesto: {presupuesto.nombre}")  # Para depuración
        self._index_presupuesto_editar = index

        # Cargar datos del presupuesto en el overlay
        self._limpiar_vista_presupuesto()
        self._actualizar_banderas(True)
        self._cargar_datos_presupuesto(presupuesto)

        # Cambiar el título del modal
        self._vista.overlay.ui.lbl_nombre_modal.setText("Editar Presupuesto")
        self._vista.overlay.ui.btn_crear_presupuesto.setText("Guardar")
        self._vista.overlay.ui.btn_borrar_presupuesto.show()
        self._vista.overlay.ui.btn_borrar_presupuesto.clicked.connect(
            lambda: self.borrar_presupuesto(index)
        )

        # Mostrar el overlay
        self._vista.overlay.show()

    def _limpiar_vista_presupuesto(self):
        """Limpia el formulario para ingresar un nuevo formulario"""
        self._vista.overlay.ui.lbl_nombre_modal.setText("Crear Nuevo Presupuesto")
        # Cargar datos básicos
        self._vista.overlay.ui.txt_nombre_presupuesto.clear()
        self._vista.overlay.ui.txt_limite_presupuesto.clear()

        # Cargar fechas
        self._vista.overlay.ui.fch_fecha_inicio.setDate(QDate.currentDate())
        self._vista.overlay.ui.fch_fecha_fin.setDate(QDate.currentDate().addMonths(1))

        # Cargar categorías (ajusta según tu modelo de datos)
        self._categorias_agregadas = copy.deepcopy(self._categorias_base)

        self.actualizar_vista_categorias()
        self._vista.overlay.ui.ptxt_notas.clear()
        self._vista.overlay.ui.cbx_recibir_notificaciones.setChecked(False)

    def _cargar_datos_presupuesto(self, presupuesto):
        """Carga los datos de un presupuesto en el formulario de edición"""
        # Cargar datos básicos
        self._vista.overlay.ui.txt_nombre_presupuesto.setText(presupuesto.nombre)
        self._vista.overlay.ui.txt_limite_presupuesto.setText(str(presupuesto.limite))

        # Cargar fechas
        self._vista.overlay.ui.fch_fecha_inicio.setDate(QDate.fromString(presupuesto.inicio_presupuesto.isoformat(), "yyyy-MM-dd"))
        self._vista.overlay.ui.fch_fecha_fin.setDate(QDate.fromString(presupuesto.fin_presupuesto.isoformat(), "yyyy-MM-dd"))

        # Cargar categorías (ajusta según tu modelo de datos)
        self._categorias_agregadas = copy.deepcopy(presupuesto.categorias)
        # for categoria in presupuesto.categorias:
        #     self._categorias_agregadas[categoria.nombre] = True  # True indica que no se puede eliminar

        self.actualizar_vista_categorias()

        # Cargar notas si las hay
        if hasattr(presupuesto, 'notas') and presupuesto.notas:
            self._vista.overlay.ui.ptxt_notas.setPlainText(presupuesto.notas)

        # Cargar configuración de notificaciones si existe
        if hasattr(presupuesto, 'notificaciones_activas'):
            self._vista.overlay.ui.cbx_recibir_notificaciones.setChecked(presupuesto.notificaciones_activas)

    def _actualizar_banderas(self, valor: bool = False):
        self.nombre_valido = valor
        self.limite_valido = valor
        self.fecha_fin_valido = True
        self.fecha_inicio_valido = True

    def borrar_presupuesto(self, index: int):
        respuesta = QMessageBox.question(
            self._vista.overlay,
            "Confirmar eliminación",
            f"̉¿Estás seguro de que quieres eliminar este presupuesto?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            self._usuario.presupuestos.pop(index)
            ManejadorArchivos.guardar_archivo(self._usuario.id, self._usuario)
            self._actualizar_banderas()
            self.actualizar_vista_presupuestos()
            self._vista.ocultar_modal(False)
            self.sender().disconnect()
