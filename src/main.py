import sys
from PyQt6.QtWidgets import QApplication

from src.controlador.c_principal import CPrincipal


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.controlador_principal = CPrincipal()

if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())