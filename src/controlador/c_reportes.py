from decimal import Decimal
import calendar
from collections import defaultdict
from decimal import Decimal

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QVBoxLayout, QHBoxLayout,
                             QLabel, QFrame, QSizePolicy, QSpacerItem)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.modelo.entidades.usuario import Usuario
from src.vista.panel_reportes import PanelReportes

# Configuración de estilo similar a shadcn/ui
plt.style.use('default')
COLORS = {
    'primary': '#0f172a',      # slate-900
    'secondary': '#64748b',    # slate-500
    'accent': '#3b82f6',       # blue-500
    'success': '#10b981',      # emerald-500
    'warning': '#f59e0b',      # amber-500
    'danger': '#ef4444',       # red-500
    'muted': '#f1f5f9',        # slate-100
    'border': '#e2e8f0',       # slate-200
    'background': '#ffffff',
    'card': '#f8fafc'          # slate-50
}

class CustomFigureCanvas(FigureCanvas):
    """Canvas personalizado con estilo shadcn"""
    def __init__(self, figure):
        super().__init__(figure)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
        """)

class CReportes:
    def __init__(self, vista: PanelReportes, usuario: Usuario):
        """
        Inicializa el widget de reportes

        Args:
            vista: QWidget donde se insertarán las gráficas
            usuario: Instancia de Usuario con los datos
        """
        self._vista = vista
        self._usuario = usuario
        self._layout_principal  = self._vista.ui.scrollAreaWidgetContents.layout()
        # Limpiar cualquier widget o layout existente en el layout principal
        self.clear_layout(self._layout_principal)


        # Generar y añadir todas las gráficas al layout principal
        self.generar_graficas(self._layout_principal)

        # Asegurar que haya un espaciador al final para empujar el contenido hacia arriba
        self._layout_principal.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def clear_layout(self, layout):
        """Método auxiliar para limpiar un layout"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                if item.layout():
                    self.clear_layout(item.layout())

    def crear_titulo_seccion(self, texto: str) -> QLabel:
        """Crea títulos de sección para cada gráfica"""
        titulo = QLabel(texto)
        titulo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        titulo.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 600;
                color: #1e293b;
                margin-bottom: 16px;
            }
        """)
        return titulo

    def crear_card_container(self) -> QFrame:
        """Crea un contenedor con estilo de card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 0;
            }
        """)
        return card

    def generar_graficas(self, layout: QVBoxLayout):
        """Genera todas las gráficas disponibles"""
        # Resumen financiero (métricas clave)
        self.crear_resumen_financiero(layout)

        # Gráfica de barras - Ingresos vs Egresos por mes
        self.crear_grafica_ingresos_egresos(layout)

        # Gráfica de pastel - Gastos por categoría
        self.crear_grafica_gastos_categoria(layout)

        # Gráfica de línea - Tendencia de balance
        self.crear_grafica_tendencia_balance(layout)

        # Gráfica de barras - Progreso de presupuestos
        self.crear_grafica_progreso_presupuestos(layout)

        # Gráfica de barras - Progreso de metas
        self.crear_grafica_progreso_metas(layout)

        # Gráfica de área - Flujo de efectivo mensual
        self.crear_grafica_flujo_efectivo(layout)

    def crear_resumen_financiero(self, layout: QVBoxLayout):
        """Crea tarjetas de resumen con métricas clave"""
        # Calcular métricas
        total_ingresos = sum(m.monto for m in self._usuario.movimientos
                             if m.tipo_movimiento.name == 'INGRESO')
        total_egresos = sum(m.monto for m in self._usuario.movimientos
                            if m.tipo_movimiento.name == 'EGRESO')
        balance = total_ingresos - total_egresos

        # Contenedor principal
        container = QVBoxLayout()
        titulo = self.crear_titulo_seccion("Resumen Financiero")
        container.addWidget(titulo)

        # Layout horizontal para las tarjetas
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        # Datos para las tarjetas
        metricas = [
            ("Total Ingresos", f"${total_ingresos:,.2f}", COLORS['success']),
            ("Total Egresos", f"${total_egresos:,.2f}", COLORS['danger']),
            ("Balance", f"${balance:,.2f}", COLORS['success'] if balance >= 0 else COLORS['danger']),
            ("Presupuestos Activos", str(len([p for p in self._usuario.presupuestos if p.esta_activo])), COLORS['accent'])
        ]

        for titulo_metric, valor, color in metricas:
            card = self.crear_tarjeta_metrica(titulo_metric, valor, color)
            cards_layout.addWidget(card)

        container.addLayout(cards_layout)
        layout.addLayout(container)

    def crear_tarjeta_metrica(self, titulo: str, valor: str, color: str) -> QFrame:
        """Crea una tarjeta individual para mostrar una métrica"""
        card = QFrame()
        card.setFixedHeight(120)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
            }}
            QFrame:hover {{
                border-color: {color};
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(8)

        # Título
        titulo_label = QLabel(titulo)
        titulo_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #64748b;
                font-weight: 500;
                padding: 0;
                border: 0;
            }
        """)

        # Valor
        valor_label = QLabel(valor)
        valor_label.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: 700;
                color: {color};
                padding: 0;
                border: 0;
            }}
        """)

        layout.addWidget(titulo_label)
        layout.addWidget(valor_label)
        layout.addStretch()

        return card

    def crear_grafica_ingresos_egresos(self, layout: QVBoxLayout):
        """Crea gráfica de barras comparando ingresos vs egresos por mes"""
        if not self._usuario.movimientos:
            return

        # Procesar datos por mes
        datos_mensuales = defaultdict(lambda: {'ingresos': Decimal('0'), 'egresos': Decimal('0')})

        for mov in self._usuario.movimientos:
            mes_key = f"{mov.fecha_transaccion.year}-{mov.fecha_transaccion.month:02d}"
            if mov.tipo_movimiento.name == 'INGRESO':
                datos_mensuales[mes_key]['ingresos'] += mov.monto
            else:
                datos_mensuales[mes_key]['egresos'] += mov.monto

        if not datos_mensuales:
            return

        # Crear gráfica
        fig = Figure(figsize=(12, 6), facecolor='white')
        ax = fig.add_subplot(111)

        meses = sorted(datos_mensuales.keys())
        ingresos = [float(datos_mensuales[mes]['ingresos']) for mes in meses]
        egresos = [float(datos_mensuales[mes]['egresos']) for mes in meses]

        x = range(len(meses))
        width = 0.35

        ax.bar([i - width/2 for i in x], ingresos, width, label='Ingresos',
               color=COLORS['success'], alpha=0.8)
        ax.bar([i + width/2 for i in x], egresos, width, label='Egresos',
               color=COLORS['danger'], alpha=0.8)

        ax.set_xlabel('Mes', fontsize=12, color=COLORS['secondary'])
        ax.set_ylabel('Monto ($)', fontsize=12, color=COLORS['secondary'])
        ax.set_xticks(x)
        ax.set_xticklabels([self.formatear_mes(mes) for mes in meses], rotation=45)
        ax.legend(frameon=False)
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax.set_facecolor('white')

        # Estilo
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['border'])
        ax.spines['bottom'].set_color(COLORS['border'])

        fig.tight_layout()

        # Agregar al layout
        container = QVBoxLayout()
        titulo = self.crear_titulo_seccion("Ingresos vs Egresos Mensuales")
        container.addWidget(titulo)

        canvas = CustomFigureCanvas(fig)
        canvas.setFixedHeight(400)
        container.addWidget(canvas)

        layout.addLayout(container)

    def crear_grafica_gastos_categoria(self, layout: QVBoxLayout):
        """Crea gráfica de pastel para gastos por categoría"""
        egresos_por_categoria = defaultdict(Decimal)

        for mov in self._usuario.movimientos:
            if mov.tipo_movimiento.name == 'EGRESO' and mov.categoria:
                egresos_por_categoria[mov.categoria] += mov.monto

        if not egresos_por_categoria:
            return

        # Crear gráfica
        fig = Figure(figsize=(10, 8), facecolor='white')
        ax = fig.add_subplot(111)

        categorias = list(egresos_por_categoria.keys())
        valores = [float(egresos_por_categoria[cat]) for cat in categorias]

        # Colores personalizados
        colores = [COLORS['primary'], COLORS['accent'], COLORS['success'],
                   COLORS['warning'], COLORS['danger'], COLORS['secondary']]
        colores = colores * (len(categorias) // len(colores) + 1)

        wedges, texts, autotexts = ax.pie(valores, labels=categorias, autopct='%1.1f%%',
                                          colors=colores[:len(categorias)], startangle=90)

        # Estilo del texto
        for text in texts:
            text.set_fontsize(11)
            text.set_color(COLORS['primary'])

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)

        ax.set_facecolor('white')

        # Agregar al layout
        container = QVBoxLayout()
        titulo = self.crear_titulo_seccion("Distribución de Gastos por Categoría")
        container.addWidget(titulo)

        canvas = CustomFigureCanvas(fig)
        canvas.setFixedHeight(500)
        container.addWidget(canvas)

        layout.addLayout(container)

    def crear_grafica_tendencia_balance(self, layout: QVBoxLayout):
        """Crea gráfica de línea mostrando la tendencia del balance"""
        if not self._usuario.movimientos:
            return

        # Ordenar movimientos por fecha
        movimientos_ordenados = sorted(self._usuario.movimientos,
                                       key=lambda x: x.fecha_transaccion)

        fechas = []
        balance_acumulado = []
        balance_actual = Decimal('0')

        for mov in movimientos_ordenados:
            fechas.append(mov.fecha_transaccion)
            if mov.tipo_movimiento.name == 'INGRESO':
                balance_actual += mov.monto
            else:
                balance_actual -= mov.monto
            balance_acumulado.append(float(balance_actual))

        # Crear gráfica
        fig = Figure(figsize=(12, 6), facecolor='white')
        ax = fig.add_subplot(111)

        ax.plot(fechas, balance_acumulado, linewidth=3, color=COLORS['accent'],
                marker='o', markersize=4, alpha=0.8)

        # Área bajo la curva
        ax.fill_between(fechas, balance_acumulado, alpha=0.3, color=COLORS['accent'])

        ax.set_xlabel('Fecha', fontsize=12, color=COLORS['secondary'])
        ax.set_ylabel('Balance Acumulado ($)', fontsize=12, color=COLORS['secondary'])
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

        # Formato de fechas
        if len(fechas) > 10:
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))

        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        # Estilo
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['border'])
        ax.spines['bottom'].set_color(COLORS['border'])
        ax.set_facecolor('white')

        fig.tight_layout()

        # Agregar al layout
        container = QVBoxLayout()
        titulo = self.crear_titulo_seccion("Tendencia del Balance")
        container.addWidget(titulo)

        canvas = CustomFigureCanvas(fig)
        canvas.setFixedHeight(400)
        container.addWidget(canvas)

        layout.addLayout(container)

    def crear_grafica_progreso_presupuestos(self, layout: QVBoxLayout):
        """Crea gráfica de barras horizontales para el progreso de presupuestos"""
        if not self._usuario.presupuestos:
            return

        presupuestos_activos = [p for p in self._usuario.presupuestos if p.esta_activo]
        if not presupuestos_activos:
            return

        # Crear gráfica
        fig = Figure(figsize=(12, max(6, len(presupuestos_activos) * 0.8)), facecolor='white')
        ax = fig.add_subplot(111)

        nombres = []
        porcentajes = []
        colores = []

        for presupuesto in presupuestos_activos:
            porcentaje = float(presupuesto.obtener_porcentaje(self._usuario.movimientos))
            nombres.append(presupuesto.nombre)
            porcentajes.append(min(porcentaje, 100))  # Limitar a 100%

            # Color según el porcentaje
            if porcentaje < 50:
                colores.append(COLORS['success'])
            elif porcentaje < 80:
                colores.append(COLORS['warning'])
            else:
                colores.append(COLORS['danger'])

        y_pos = range(len(nombres))
        bars = ax.barh(y_pos, porcentajes, color=colores, alpha=0.8, height=0.6)

        # Agregar porcentajes en las barras
        for i, (bar, porcentaje) in enumerate(zip(bars, porcentajes)):
            width = bar.get_width()
            ax.text(width + 2, bar.get_y() + bar.get_height()/2,
                    f'{porcentaje:.1f}%', ha='left', va='center', fontweight='bold')

        ax.set_yticks(y_pos)
        ax.set_yticklabels(nombres)
        ax.set_xlabel('Porcentaje Utilizado (%)', fontsize=12, color=COLORS['secondary'])
        ax.set_xlim(0, max(110, max(porcentajes) + 10))

        # Línea de referencia en 100%
        ax.axvline(x=100, color=COLORS['danger'], linestyle='--', alpha=0.7, linewidth=2)

        # Estilo
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['border'])
        ax.spines['bottom'].set_color(COLORS['border'])
        ax.set_facecolor('white')
        ax.grid(True, alpha=0.3, axis='x')

        fig.tight_layout()

        # Agregar al layout
        container = QVBoxLayout()
        titulo = self.crear_titulo_seccion("Progreso de Presupuestos")
        container.addWidget(titulo)

        canvas = CustomFigureCanvas(fig)
        canvas.setFixedHeight(max(300, len(presupuestos_activos) * 60 + 100))
        container.addWidget(canvas)

        layout.addLayout(container)

    def crear_grafica_progreso_metas(self, layout: QVBoxLayout):
        """Crea gráfica de barras horizontales para el progreso de metas"""
        if not self._usuario.metas:
            return

        metas_activas = [m for m in self._usuario.metas if m.esta_activo]
        if not metas_activas:
            return

        # Crear gráfica
        fig = Figure(figsize=(12, max(6, len(metas_activas) * 0.8)), facecolor='white')
        ax = fig.add_subplot(111)

        nombres = []
        porcentajes = []
        colores = []

        for meta in metas_activas:
            meta.obtener_monto_reunido(self._usuario.movimientos)
            porcentaje = float(meta.obtener_porcentaje())
            nombres.append(meta.nombre)
            porcentajes.append(min(porcentaje, 100))  # Limitar a 100%

            # Color según el porcentaje
            if porcentaje >= 100:
                colores.append(COLORS['success'])
            elif porcentaje >= 75:
                colores.append(COLORS['accent'])
            elif porcentaje >= 50:
                colores.append(COLORS['warning'])
            else:
                colores.append(COLORS['secondary'])

        y_pos = range(len(nombres))
        bars = ax.barh(y_pos, porcentajes, color=colores, alpha=0.8, height=0.6)

        # Agregar porcentajes en las barras
        for i, (bar, porcentaje) in enumerate(zip(bars, porcentajes)):
            width = bar.get_width()
            ax.text(width + 2, bar.get_y() + bar.get_height()/2,
                    f'{porcentaje:.1f}%', ha='left', va='center', fontweight='bold')

        ax.set_yticks(y_pos)
        ax.set_yticklabels(nombres)
        ax.set_xlabel('Porcentaje Completado (%)', fontsize=12, color=COLORS['secondary'])
        ax.set_xlim(0, max(110, max(porcentajes) + 10))

        # Línea de referencia en 100%
        ax.axvline(x=100, color=COLORS['success'], linestyle='--', alpha=0.7, linewidth=2)

        # Estilo
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['border'])
        ax.spines['bottom'].set_color(COLORS['border'])
        ax.set_facecolor('white')
        ax.grid(True, alpha=0.3, axis='x')

        fig.tight_layout()

        # Agregar al layout
        container = QVBoxLayout()
        titulo = self.crear_titulo_seccion("Progreso de Metas")
        container.addWidget(titulo)

        canvas = CustomFigureCanvas(fig)
        canvas.setFixedHeight(max(300, len(metas_activas) * 60 + 100))
        container.addWidget(canvas)

        layout.addLayout(container)

    def crear_grafica_flujo_efectivo(self, layout: QVBoxLayout):
        """Crea gráfica de área para mostrar el flujo de efectivo mensual"""
        if not self._usuario.movimientos:
            return

        # Procesar datos por mes
        datos_mensuales = defaultdict(lambda: {'ingresos': Decimal('0'), 'egresos': Decimal('0')})

        for mov in self._usuario.movimientos:
            mes_key = f"{mov.fecha_transaccion.year}-{mov.fecha_transaccion.month:02d}"
            if mov.tipo_movimiento.name == 'INGRESO':
                datos_mensuales[mes_key]['ingresos'] += mov.monto
            else:
                datos_mensuales[mes_key]['egresos'] += mov.monto

        if not datos_mensuales:
            return

        # Crear gráfica
        fig = Figure(figsize=(12, 6), facecolor='white')
        ax = fig.add_subplot(111)

        meses = sorted(datos_mensuales.keys())
        ingresos = [float(datos_mensuales[mes]['ingresos']) for mes in meses]
        egresos = [float(datos_mensuales[mes]['egresos']) for mes in meses]
        flujo_neto = [ing - egr for ing, egr in zip(ingresos, egresos)]

        x = range(len(meses))

        # Áreas apiladas
        ax.fill_between(x, 0, ingresos, alpha=0.7, color=COLORS['success'], label='Ingresos')
        ax.fill_between(x, 0, [-egr for egr in egresos], alpha=0.7, color=COLORS['danger'], label='Egresos')
        ax.plot(x, flujo_neto, linewidth=3, color=COLORS['primary'], marker='o', markersize=6, label='Flujo Neto')

        ax.set_xlabel('Mes', fontsize=12, color=COLORS['secondary'])
        ax.set_ylabel('Monto ($)', fontsize=12, color=COLORS['secondary'])
        ax.set_xticks(x)
        ax.set_xticklabels([self.formatear_mes(mes) for mes in meses], rotation=45)
        ax.legend(frameon=False, loc='upper left')
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax.axhline(y=0, color=COLORS['primary'], linestyle='-', linewidth=1, alpha=0.8)

        # Estilo
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['border'])
        ax.spines['bottom'].set_color(COLORS['border'])
        ax.set_facecolor('white')

        fig.tight_layout()

        # Agregar al layout
        container = QVBoxLayout()
        titulo = self.crear_titulo_seccion("Flujo de Efectivo Mensual")
        container.addWidget(titulo)

        canvas = CustomFigureCanvas(fig)
        canvas.setFixedHeight(400)
        container.addWidget(canvas)

        layout.addLayout(container)

    def formatear_mes(self, mes_str: str) -> str:
        """Convierte formato YYYY-MM a formato legible"""
        try:
            year, month = mes_str.split('-')
            return f"{calendar.month_abbr[int(month)]} {year}"
        except:
            return mes_str