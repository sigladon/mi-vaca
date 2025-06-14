from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QFrame, QVBoxLayout, QHBoxLayout

from src.vista.ui.ventana_principal_ui import Ui_VentanaPrincipal


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self._ui = Ui_VentanaPrincipal()
        self._ui.setupUi(self)

        self.sidebar = QFrame()
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar.setFixedWidth(200)

        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)


        self.contenedor_principal = QWidget()
        self.layout_principal = QHBoxLayout(self.contenedor_principal)
        self.layout_principal.setContentsMargins(0,0,0,0)

        self.vista_central = QWidget()
        self.layout_principal.addWidget(self.sidebar)
        self.layout_principal.addWidget(self.vista_central)
        self.setCentralWidget(self.contenedor_principal)