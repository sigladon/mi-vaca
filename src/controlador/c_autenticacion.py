from datetime import date

from src.vista.login import Ui_LoginWindow as VentanaLogin
from src.utils.manejador_archivos import ManejadorArchivos as MA
class ControladorAutenticacion:
    def __init__(self):
        super(ventanaPrincipal, self).__init__(parent)
        self.setupUi(self)
        self.actionAgregar.triggered.connect(self.ingreso_datos)
        self.actionListar.triggered.connect(self.acercade)
        self.actionListar_Usuarios.triggered.connect(self.listado_datos)


