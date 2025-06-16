import re
from datetime import date
from decimal import Decimal, InvalidOperation

from PyQt6.QtCore import QObject, QDate, Qt
from PyQt6.QtWidgets import QLineEdit, QDateEdit, QWidget, QHBoxLayout, QLabel, QPushButton, QMessageBox, QVBoxLayout

from src.modelo.entidades.meta import Meta
from src.modelo.entidades.usuario import Usuario
from src.utils.manejador_archivos import ManejadorArchivos
from src.vista.overlay_meta import OverlayMeta
from src.vista.panel_metas import PanelMetas


class CMetas(QObject):
    def __init__(self, vista: PanelMetas, usuario: Usuario):
        super().__init__()
        self.nombre_valido = None
        self.monto_objetivo_valido = False
        self.monto_actual_valido = True  # Es opcional, por eso True por defecto
        self.fecha_limite_valido = True
        self._index_meta_editar = None
        self._vista = vista
        self._usuario = usuario

        self._vista.overlay = OverlayMeta(self._vista)
        self._vista.overlay.ui.txt_nombre_meta.editingFinished.connect(self.verificar_nombre)
        self._vista.overlay.ui.txt_monto_objetivo.editingFinished.connect(self.verificar_monto_objetivo)
        self._vista.overlay.ui.txt_monto_actual.editingFinished.connect(self.verificar_monto_actual)
        self._vista.overlay.ui.fch_limite.editingFinished.connect(self.verificar_fecha_limite)
        self._vista.ui.btn_nueva_meta.clicked.connect(self.mostrar_modal)
        self._vista.overlay.ui.btn_crear_meta.clicked.connect(self.guardar_meta)

        self.actualizar_vista_metas()

    def mostrar_modal(self):
        self._actualizar_banderas()
        self._limpiar_vista_meta()
        self._index_meta_editar = None
        self._vista.overlay.ui.btn_crear_meta.setText("Crear Meta")
        self._vista.mostrar_modal()

    def verificar_nombre(self):
        txt_nombre: QLineEdit = self.sender()
        nombre = txt_nombre.text()
        if nombre == "":
            txt_nombre.setStyleSheet("")
            self.nombre_valido = False
        elif not self.validar_nombre(nombre):
            print("El nombre de la meta no es válido")  # Para depuración
            txt_nombre.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.nombre_valido = False
        else:
            txt_nombre.setStyleSheet("")
            self.nombre_valido = True

    def verificar_monto_objetivo(self):
        txt_monto: QLineEdit = self.sender()
        monto = txt_monto.text()
        if monto == "":
            txt_monto.setStyleSheet("")
            self.monto_objetivo_valido = False
        elif not self._validar_decimal(monto):
            print("El monto objetivo no es válido")  # Para depuración
            txt_monto.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.monto_objetivo_valido = False
        elif Decimal(monto) <= 0:
            print("El monto objetivo debe ser mayor a cero")  # Para depuración
            txt_monto.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.monto_objetivo_valido = False
        else:
            txt_monto.setStyleSheet("")
            self.monto_objetivo_valido = True

    def verificar_monto_actual(self):
        txt_monto: QLineEdit = self.sender()
        monto = txt_monto.text()
        if monto == "":
            txt_monto.setStyleSheet("")
            self.monto_actual_valido = True  # Es opcional
        elif not self._validar_decimal(monto):
            print("El monto actual no es válido")  # Para depuración
            txt_monto.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.monto_actual_valido = False
        elif Decimal(monto) < 0:
            print("El monto actual no puede ser negativo")  # Para depuración
            txt_monto.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.monto_actual_valido = False
        else:
            txt_monto.setStyleSheet("")
            self.monto_actual_valido = True

    def verificar_fecha_limite(self):
        fch_fecha_limite: QDateEdit = self.sender()
        fecha_limite = fch_fecha_limite.date().toPyDate()
        fecha_hoy = date.today()

        if fecha_limite > fecha_hoy:
            fch_fecha_limite.setStyleSheet("")
            self.fecha_limite_valido = True
        else:
            print("La fecha límite debe ser posterior a hoy")  # Para depuración
            fch_fecha_limite.setStyleSheet("border: 1px solid red;")
            self.fecha_limite_valido = False

    def guardar_meta(self):
        if not (self.nombre_valido and self.monto_objetivo_valido and
                self.monto_actual_valido and self.fecha_limite_valido):
            QMessageBox.warning(
                self._vista.overlay,
                "Error",
                "Existen datos incorrectos"
            )
            return

        aux = Decimal('0.01')
        nombre = self._vista.overlay.ui.txt_nombre_meta.text()
        monto_objetivo = Decimal(self._vista.overlay.ui.txt_monto_objetivo.text()).quantize(aux)

        monto_actual_text = self._vista.overlay.ui.txt_monto_actual.text()
        monto_actual = Decimal(monto_actual_text).quantize(aux) if monto_actual_text else Decimal('0.00')

        fecha_limite = self._vista.overlay.ui.fch_limite.date().toPyDate()
        descripcion = self._vista.overlay.ui.ptxt_descripcion.toPlainText()

        if self._index_meta_editar is None:
            nueva_meta = Meta(
                nombre=nombre,
                monto_objetivo=monto_objetivo,
                fecha_inicio=date.today(),
                fecha_limite=fecha_limite,
                descripcion=descripcion,
                monto_base=monto_actual
            )
            self._usuario.agregar_meta(nueva_meta)
        else:
            meta_editada = self._usuario.metas[self._index_meta_editar]
            meta_editada.nombre = nombre
            meta_editada.monto_objetivo = monto_objetivo
            meta_editada.monto_base = monto_actual
            meta_editada.fecha_limite = fecha_limite
            meta_editada.descripcion = descripcion

        print(self._usuario.metas)

        ManejadorArchivos.guardar_archivo(self._usuario.id, self._usuario)

        QMessageBox.information(
            self._vista.overlay,
            "Registro exitoso",
            "La meta se guardó exitosamente"
        )

        self.actualizar_vista_metas()
        self._vista.ocultar_modal(False)

    def actualizar_vista_metas(self):
        container_widget = self._vista.ui.contenedor_metas.widget()

        if container_widget is None:
            return

        layout = container_widget.layout()

        if layout is None:
            layout = QVBoxLayout(container_widget)
            layout.setObjectName("verticalLayout_5")
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(8)

        self._limpiar_layout(layout)

        if not self._usuario.metas:
            lbl_vacio = QLabel("No tienes metas aún. Prueba creando una.")
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
            for index, meta in enumerate(self._usuario.metas):
                widget_meta = self._crear_widget_meta(index, meta)
                layout.addWidget(widget_meta)

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
                    try:
                        widget.setParent(None)
                    except TypeError:
                        pass
                    finally:
                        widget.deleteLater()

    def _crear_widget_meta(self, index, meta):
        widget_meta = QWidget()
        widget_meta.setObjectName(f"meta_{meta.id}")
        widget_meta.setFixedHeight(160)
        widget_meta.setStyleSheet("""
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

        layout_principal = QHBoxLayout(widget_meta)
        layout_principal.setContentsMargins(24, 8, 24, 8)
        layout_principal.setSpacing(4)

        layout_info = QVBoxLayout()
        layout_info.setSpacing(4)

        layout_nombre = QHBoxLayout()
        layout_nombre.setSpacing(10)

        lbl_nombre = QLabel(meta.nombre)
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

        lbl_estado = QLabel("ACTIVA" if meta.esta_activo else "INACTIVA")
        estado_color = "#28a745" if meta.esta_activo else "#6c757d"
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


        aux = Decimal("0.01")
        lbl_objetivo = QLabel(f"Objetivo: ${meta.monto_objetivo.quantize(aux)}")
        lbl_objetivo.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #495057;
                background: transparent;
                border: none;
                padding: 0;
            }
        """)
        layout_info.addWidget(lbl_objetivo)

        lbl_actual = QLabel(f"Actual: ${meta.obtener_monto_reunido(self._usuario.movimientos).quantize(aux)}")
        porcentaje = meta.obtener_porcentaje()
        color_actual = "#28a745" if porcentaje >= 100 else "#007bff" if porcentaje >= 50 else "#ffc107"
        lbl_actual.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                color: {color_actual};
                font-weight: 500;
                background: transparent;
                border: none;
                padding: 0;
            }}
        """)
        layout_info.addWidget(lbl_actual)

        # Barra de progreso personalizada
        widget_progreso = self._crear_barra_progreso(porcentaje)
        layout_info.addWidget(widget_progreso)

        # Etiqueta de porcentaje
        lbl_porcentaje = QLabel(f"{porcentaje:.1f}%")
        lbl_porcentaje.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: bold;
                color: {color_actual};
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
        btn_editar.clicked.connect(lambda: self.editar_meta(index, meta))
        layout_principal.addWidget(btn_editar)

        return widget_meta

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
            color_progreso = "#28a745"  # Verde - completado
        elif porcentaje >= 50:
            color_progreso = "#007bff"  # Azul - buen progreso
        else:
            color_progreso = "#ffc107"  # Amarillo - progreso inicial

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

    def editar_meta(self, index, meta):
        """Abre el modal para editar una meta existente"""
        print(f"Editando meta: {meta.nombre}")  # Para depuración
        self._index_meta_editar = index

        # Cargar datos de la meta en el overlay
        self._limpiar_vista_meta()
        self._actualizar_banderas(True)
        self._cargar_datos_meta(meta)

        # Cambiar el título del modal
        self._vista.overlay.ui.label.setText("Editar Meta")
        self._vista.overlay.ui.btn_crear_meta.setText("Guardar")

        self._vista.overlay.ui.btn_borrar_meta.clicked.connect(
            lambda: self.borrar_meta(index)
        )
        self._vista.mostrar_modal(True)

    def _limpiar_vista_meta(self):
        """Limpia el formulario para ingresar una nueva meta"""
        self._vista.overlay.ui.label.setText("Crear Nueva Meta")
        self._vista.overlay.ui.txt_nombre_meta.clear()
        self._vista.overlay.ui.txt_monto_objetivo.clear()
        self._vista.overlay.ui.txt_monto_actual.clear()
        self._vista.overlay.ui.fch_limite.setDate(QDate.currentDate().addMonths(1))
        self._vista.overlay.ui.ptxt_descripcion.clear()

    def _cargar_datos_meta(self, meta):
        """Carga los datos de una meta en el formulario de edición"""
        self._vista.overlay.ui.txt_nombre_meta.setText(meta.nombre)
        self._vista.overlay.ui.txt_monto_objetivo.setText(str(meta.monto_objetivo))
        self._vista.overlay.ui.txt_monto_actual.setText(str(meta.monto_base))
        self._vista.overlay.ui.fch_limite.setDate(
            QDate.fromString(meta.fecha_limite.isoformat(), "yyyy-MM-dd")
        )

        if meta.descripcion:
            self._vista.overlay.ui.ptxt_descripcion.setPlainText(meta.descripcion)

    def _actualizar_banderas(self, valor: bool = False):
        self.nombre_valido = valor
        self.monto_objetivo_valido = valor
        self.monto_actual_valido = True  # Siempre es válido porque es opcional
        self.fecha_limite_valido = True

    @staticmethod
    def validar_nombre(nombre):
        """Valida que el nombre tenga entre 2 y 50 caracteres y solo contenga letras, espacios y apostrofes"""
        regex_nombre = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ' ]{2,50}$")
        return regex_nombre.match(nombre)

    @staticmethod
    def _validar_decimal(texto: str) -> bool:
        """Valida que el texto sea un número decimal válido"""
        try:
            Decimal(texto)
            return True
        except InvalidOperation:
            return False


    def borrar_meta(self, index: int):
        """Elimina una meta después de confirmar con el usuario"""
        meta = self._usuario.metas[index]

        respuesta = QMessageBox.question(
            self._vista.overlay,
            "Confirmar eliminación",
            f"¿Estás seguro de que quieres eliminar la meta '{meta.nombre}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            # Eliminar la meta de la lista
            self._usuario.metas.pop(index)

            # Guardar los cambios
            ManejadorArchivos.guardar_archivo(self._usuario.id, self._usuario)

            # Mostrar mensaje de confirmación
            QMessageBox.information(
                self._vista.overlay,
                "Meta eliminada",
                f"La meta '{meta.nombre}' ha sido eliminada exitosamente"
            )

            # Actualizar la vista y cerrar el modal
            self._actualizar_banderas()
            self.actualizar_vista_metas()
            self._vista.ocultar_modal(False)

            # Desconectar la señal para evitar conexiones múltiples
            self.sender().disconnect()


