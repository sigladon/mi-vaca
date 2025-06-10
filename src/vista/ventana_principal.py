from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QSizePolicy, QFrame, QVBoxLayout, QHBoxLayout, \
    QPushButton

from src.controlador.c_login import CLogin
from src.controlador.c_registro import CRegistro
from src.utils.manejador_archivos import ManejadorArchivos
from src.vista.login import Login
from src.vista.panel_bienvenida import PanelBienvenida
from src.vista.panel_metas import PanelMetas
from src.vista.panel_presupuestos import PanelPresupuesto
from src.vista.panel_transacciones import PanelTransacciones
from src.vista.registrarse import Registrarse
from src.vista.ui.ventana_principal_ui import Ui_VentanaPrincipal


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.panel_presupuestos = None
        self.panel_transacciones = None
        self.panel_metas = None
        self.panel_bienvenida = None
        self.vista_registrarse = None
        self.c_registro = None
        self.vista_login = None
        self.c_login = None
        self.usuario = None
        self._ui = Ui_VentanaPrincipal()
        self._ui.setupUi(self)

        self.sidebar = QFrame()
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar.setFixedWidth(200)

        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.sidebar_layout.addWidget(self.crear_boton("Dashboard", lambda: print("Dashboard")))
        self.sidebar_layout.addWidget(self.crear_boton("Presupuestos", self.mostrar_vista_presupuestos))
        self.sidebar_layout.addWidget(self.crear_boton("Transacciones", self.mostrar_vista_transacciones))
        self.sidebar_layout.addWidget(self.crear_boton("Metas Financieras", self.mostrar_vista_metas))
        self.sidebar_layout.addWidget(self.crear_boton("Reportes", lambda: print("Reportes")))
        self.sidebar_layout.addWidget(self.crear_boton("Configuración", lambda: print("Configuración")))
        self.sidebar_layout.addWidget(self.crear_boton("Acerca de...", lambda: print("Acerca de")))
        self.sidebar_layout.addStretch()
        self.sidebar_layout.addWidget(self.crear_boton("Cerrar Sesión", self.cerrar_sesion))

        self.contenedor_principal = QWidget()
        self.layout_principal = QHBoxLayout(self.contenedor_principal)
        self.layout_principal.setContentsMargins(0,0,0,0)

        self.vista_central = QWidget()
        self.layout_principal.addWidget(self.sidebar)
        self.layout_principal.addWidget(self.vista_central)
        self.setCentralWidget(self.contenedor_principal)


        self.token = ManejadorArchivos.cargar_archivo("token", None)
        if self.token is None:
            self.mostrar_vista_login()
        else:
            self.mostrar_vista_bienvenida()

    def crear_boton(self, texto, callback):
        boton = QPushButton(texto)
        boton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        boton.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding-left: 12px;
                min-width: 160px;
                max-width: 160px;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
        """)
        boton.clicked.connect(callback)
        return boton

    def cambiar_vista_central(self, nueva_vista: QWidget):
        self.layout_principal.replaceWidget(self.vista_central, nueva_vista)
        self.vista_central.deleteLater()
        self.vista_central = nueva_vista

    def mostrar_vista_login(self):
        self.sidebar.hide()
        self.c_login = CLogin(self.token)
        self.vista_login = Login(self.token, self.c_login)
        self.vista_login.solicitar_mostrar_registro.connect(self.mostrar_vista_registrarse)
        self.vista_login.solicitar_mostrar_bienvenida.connect(self.mostrar_vista_bienvenida)
        self.cambiar_vista_central(self.vista_login)
        self.setWindowTitle("Sistema de Gestión Financiera - Login")

    def mostrar_vista_registrarse(self):
        self.c_registro = CRegistro()
        self.vista_registrarse = Registrarse(self.c_registro)
        self.cambiar_vista_central(self.vista_registrarse)
        self.setWindowTitle("Sistema de Gestión Financiera - Registrarse")
        self.vista_registrarse.solicitar_mostrar_login.connect(self.mostrar_vista_login)

    def mostrar_vista_bienvenida(self):
        self.sidebar.show()
        self.usuario = ManejadorArchivos.cargar_archivo(self.token.uuid, None)
        self.panel_bienvenida = PanelBienvenida(self.usuario)
        self.cambiar_vista_central(self.panel_bienvenida)
        self.setWindowTitle("Sistema de Gestión Financiera - Bienvenida")

    def mostrar_vista_metas(self):
        self.panel_metas = PanelMetas(self.usuario)
        self.cambiar_vista_central(self.panel_metas)
        self.setWindowTitle("Sistema de Gestión Financiera - Metas")

    def mostrar_vista_transacciones(self):
        self.panel_transacciones = PanelTransacciones(self.usuario)
        self.cambiar_vista_central(self.panel_transacciones)
        self.setWindowTitle("Sistema de Gestión Financiera - Transacciones")

    def mostrar_vista_presupuestos(self):
        self.panel_presupuestos = PanelPresupuesto(self.usuario)
        self.cambiar_vista_central(self.panel_presupuestos)
        self.setWindowTitle("Sistema de Gestión Financiera - Presupuestos")

    def cerrar_sesion(self):
        ManejadorArchivos.borrar_archivo("token")
        self.mostrar_vista_login()