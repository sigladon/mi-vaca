import sys
from PyQt6.QtWidgets import QApplication

from src.vista.ventana_principal import VentanaPrincipal


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.ventana_principal = VentanaPrincipal()
        self.ventana_principal.show()

if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())