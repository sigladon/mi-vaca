from PyQt6.QtCore import QObject, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QPushButton, QSizePolicy, QMessageBox

from src.controlador.c_metas import CMetas
from src.controlador.c_presupuestos import CPresupuestos
from src.controlador.c_reportes import CReportes
from src.controlador.c_transacciones import CTransaccion
from src.controlador.c_usuario import CUsuario
from src.utils.manejador_archivos import ManejadorArchivos
from src.vista.panel_acerca_de import PanelAcercaDe
from src.vista.panel_login import Login
from src.vista.panel_bienvenida import PanelBienvenida
from src.vista.panel_metas import PanelMetas
from src.vista.panel_presupuestos import PanelPresupuesto
from src.vista.panel_reportes import PanelReportes
from src.vista.panel_transacciones import PanelTransacciones
from src.vista.panel_registrarse import Registrarse
from src.vista.ventana_principal import VentanaPrincipal


class CPrincipal(QObject):
    def __init__(self):
        super().__init__()
        self.c_reportes = None
        self.nombre_programa = "Mi vaca"
        self.c_transaccion = None
        self.c_presupuesto = None
        self._usuario = None
        self.c_usuario = None
        self._vista = VentanaPrincipal()
        self._vista.show()
        # self._vista.sidebar_layout.addWidget(self._crear_boton("Dashboard", lambda: print("Dashboard")))
        self._vista.sidebar_layout.addWidget(self._crear_boton("Presupuestos", "presupuestos", self.mostrar_vista_presupuestos))
        self._vista.sidebar_layout.addWidget(self._crear_boton("Transacciones", "transacciones", self.mostrar_vista_transacciones))
        self._vista.sidebar_layout.addWidget(self._crear_boton("Metas Financieras", "metas_financieras", self.mostrar_vista_metas))
        self._vista.sidebar_layout.addWidget(self._crear_boton("Reportes", "reportes", self.mostrar_vista_reportes))
        # self._vista.sidebar_layout.addWidget(self._crear_boton("Configuración", lambda: print("Configuración")))
        self._vista.sidebar_layout.addWidget(self._crear_boton("Acerca de...", "about", self.mostrar_vista_acerca_de))
        self._vista.sidebar_layout.addStretch()
        self._vista.sidebar_layout.addWidget(self._crear_boton("Cerrar Sesión", "cerrar_sesion", self.cerrar_sesion))

        self.token = ManejadorArchivos.cargar_archivo("token",None)
        if self.token is None:
            print("Mostrando login")
            self.c_usuario = CUsuario(Login())
            self.mostrar_vista_login()
        else:
            print("Mostrando bienvenida")
            self.mostrar_vista_bienvenida()

    @staticmethod
    def _crear_boton(texto, icono, callback):
        boton = QPushButton(texto)
        boton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        boton.setIcon(QIcon(f"./assets/iconos/{icono}.svg"))
        boton.setIconSize(QSize(24,24))
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
        self._vista.sidebar.show()
        token = ManejadorArchivos.cargar_archivo("token", None)
        self._usuario = ManejadorArchivos.cargar_archivo(token.uuid, None)
        panel_bienvenida = PanelBienvenida(self._usuario)
        self.cambiar_vista_central(panel_bienvenida)
        self._vista.setWindowTitle("Sistema de Gestión Financiera - Bienvenida")

    def mostrar_vista_metas(self):
        panel_metas = PanelMetas()
        self.c_metas = CMetas(panel_metas, self._usuario)
        self.cambiar_vista_central(panel_metas)
        self._vista.setWindowTitle("Sistema de Gestión Financiera - Metas")

    def mostrar_vista_transacciones(self):
        panel_transacciones = PanelTransacciones()
        self.c_transaccion = CTransaccion(panel_transacciones, self._usuario)
        self.cambiar_vista_central(panel_transacciones)
        self._vista.setWindowTitle("Sistema de Gestión Financiera - Transacciones")

    def mostrar_vista_presupuestos(self):
        panel_presupuestos = PanelPresupuesto()
        self.c_presupuesto = CPresupuestos(panel_presupuestos, self._usuario)
        self.cambiar_vista_central(panel_presupuestos)
        self._vista.setWindowTitle("Sistema de Gestión Financiera - Presupuestos")

    def mostrar_vista_acerca_de(self):
        panel_acerca_de = PanelAcercaDe()
        self.cambiar_vista_central(panel_acerca_de)
        self._vista.setWindowTitle(f"{self.nombre_programa} - Acerca de")

    def mostrar_vista_reportes(self):
        panel_acerca_de = PanelReportes()
        self.c_reportes = CReportes(panel_acerca_de, self._usuario)
        self.cambiar_vista_central(panel_acerca_de)
        self._vista.setWindowTitle(f"{self.nombre_programa} - Acerca de")

    def cerrar_sesion(self):
        respuesta = QMessageBox.question(
            self._vista,
            "Confirmar cerrar sesión",
            f"¿Estás seguro de querer cerrar sesión?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            ManejadorArchivos.borrar_archivo("token")
            self.mostrar_vista_login()
