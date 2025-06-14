from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget, QPushButton, QSizePolicy

from src.controlador.c_usuario import CUsuario
from src.utils.manejador_archivos import ManejadorArchivos
from src.vista.login import Login
from src.vista.registrarse import Registrarse
from src.vista.ventana_principal import VentanaPrincipal


class CPrincipal(QObject):
    def __init__(self):
        super().__init__()
        self.c_usuario = None
        self._vista = VentanaPrincipal()
        self._vista.show()
        self._vista.sidebar_layout.addWidget(self._crear_boton("Dashboard", lambda: print("Dashboard")))
        self._vista.sidebar_layout.addWidget(self._crear_boton("Presupuestos", self.mostrar_vista_presupuestos))
        self._vista.sidebar_layout.addWidget(self._crear_boton("Transacciones", self.mostrar_vista_transacciones))
        self._vista.sidebar_layout.addWidget(self._crear_boton("Metas Financieras", self.mostrar_vista_metas))
        self._vista.sidebar_layout.addWidget(self._crear_boton("Reportes", lambda: print("Reportes")))
        self._vista.sidebar_layout.addWidget(self._crear_boton("Configuración", lambda: print("Configuración")))
        self._vista.sidebar_layout.addWidget(self._crear_boton("Acerca de...", lambda: print("Acerca de")))
        self._vista.sidebar_layout.addStretch()
        self._vista.sidebar_layout.addWidget(self._crear_boton("Cerrar Sesión", self.cerrar_sesion))

        self.token = ManejadorArchivos.cargar_archivo("token",None)
        if self.token is None:
            print("Mostrando login")
            self.c_usuario = CUsuario(Login())
            self.mostrar_vista_login()
        else:
            print("Mostrando bienvenida")
            self.mostrar_vista_bienvenida()

    @staticmethod
    def _crear_boton(texto, callback):
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
        self._vista.layout_principal.replaceWidget(self._vista.vista_central, nueva_vista)
        self._vista.vista_central.deleteLater()
        self._vista.vista_central = nueva_vista

    def mostrar_vista_login(self):
        self._vista.sidebar.hide()
        vista_login = Login()
        self.c_usuario = CUsuario(vista_login)
        vista_login.solicitar_mostrar_registro.connect(self.mostrar_vista_registrarse)
        vista_login.solicitar_mostrar_bienvenida.connect(self.mostrar_vista_bienvenida)
        self.cambiar_vista_central(vista_login)
        self._vista.setWindowTitle("Sistema de Gestión Financiera - Login")

    def mostrar_vista_registrarse(self):
        vista_registrarse = Registrarse()
        self.c_usuario.cambiar_vista(vista_registrarse)
        self.cambiar_vista_central(vista_registrarse)
        self._vista.setWindowTitle("Sistema de Gestión Financiera - Registrarse")
        vista_registrarse.solicitar_mostrar_login.connect(self.mostrar_vista_login)

    def mostrar_vista_bienvenida(self):
        self.sidebar.show()
        self.usuario = ManejadorArchivos.cargar_archivo(self.token.uuid, None)
        self._vista.panel_bienvenida = PanelBienvenida(self.usuario)
        self.cambiar_vista_central(self.panel_bienvenida)
        self._vista.setWindowTitle("Sistema de Gestión Financiera - Bienvenida")

    def mostrar_vista_metas(self):
        self.panel_metas = PanelMetas(self.usuario)
        self.cambiar_vista_central(self.panel_metas)
        self._vista.setWindowTitle("Sistema de Gestión Financiera - Metas")

    def mostrar_vista_transacciones(self):
        self.panel_transacciones = PanelTransacciones(self.usuario)
        self.cambiar_vista_central(self.panel_transacciones)
        self._vista.setWindowTitle("Sistema de Gestión Financiera - Transacciones")

    def mostrar_vista_presupuestos(self):
        self.panel_presupuestos = PanelPresupuesto(self.usuario)
        self.cambiar_vista_central(self.panel_presupuestos)
        self._vista.setWindowTitle("Sistema de Gestión Financiera - Presupuestos")

    def cerrar_sesion(self):
        ManejadorArchivos.borrar_archivo("token")
        self.mostrar_vista_login()
