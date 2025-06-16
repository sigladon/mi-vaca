import re

from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QLineEdit, QWidget

from src.modelo.entidades.token import Token
from src.modelo.entidades.usuario import Usuario
from src.utils.manejador_archivos import ManejadorArchivos
from src.vista.panel_login import Login
from src.vista.panel_registrarse import Registrarse


class CUsuario(QObject):

    def __init__(self, vista):
        super().__init__()
        self.username_valido = False
        self.nombre_valido = False
        self.correo_valido = False
        self.contrasenia_valida = False
        self.contrasenia_repetida_valida = False
        self._vista = None
        self.cambiar_vista(vista)
        self._usuarios = ManejadorArchivos.cargar_archivo("usuarios", dict())


    def cambiar_vista(self, vista: Login | Registrarse):
        self._vista = vista
        if isinstance(vista,Login):
            self._vista.ui.btn_iniciar_sesion.clicked.connect(self.iniciar_sesion)
            self._vista.ui.btn_registrarse.clicked.connect(self._vista.emitir_solicitar_mostrar_registro)
        else:
            self._vista.ui.txt_username.editingFinished.connect(self.verificar_username_registro)
            self._vista.ui.txt_nombre.editingFinished.connect(self.verificar_nombre_registro)
            self._vista.ui.txt_correo.editingFinished.connect(self.verificar_correo_registro)
            self._vista.ui.txt_contrasenia.editingFinished.connect(self.verificar_contrasenia_registro)
            self._vista.ui.txt_repetir_contrasenia.editingFinished.connect(
                lambda: self.verificar_contrasenia_repetida(self._vista.ui.txt_contrasenia.text())
            )
            self._vista.ui.btn_registrarse.clicked.connect(self.registrarse)
            self._vista.ui.btn_volver.clicked.connect(self._volver_al_login)


    def verificar_username_registro(self):
        txt_username: QLineEdit = self.sender()
        username = txt_username.text()
        if username == "":
            txt_username.setStyleSheet("")
            self.username_valido = False
        elif not self._validar_username(username):
            print("El nombre de usuario ingresado no es válido") # Para depuración
            txt_username.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.username_valido = False
        elif username in self._usuarios:
            print("Ese nombre de usuario ya está siendo usado") # Para depuración
            txt_username.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.username_valido = False
        else:
            txt_username.setStyleSheet("")
            self.username_valido = True

    def verificar_nombre_registro(self):
        txt_nombre: QLineEdit = self.sender()
        nombre = txt_nombre.text()
        if nombre == "":
            print("El nombre no puedes estar vacío") # Para depuración
            txt_nombre.setStyleSheet("")
            self.nombre_valido =  False
        elif not self._validar_nombre(nombre):
            print("El nombre ingresado no es válido") # Para depuración
            txt_nombre.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.nombre_valido =  False
        else:
            txt_nombre.setStyleSheet("")
            self.nombre_valido =  True

    def verificar_correo_registro(self):
        txt_correo: QLineEdit = self.sender()
        correo = txt_correo.text()
        if not self._validar_correo(correo):
            print("El correo proporcionado no es válido") # Para depuración
            txt_correo.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.correo_valido = False
        elif correo in self._usuarios:
            print("Ya existe un usuario registrado con ese correo electrónico") # Para depuración
            txt_correo.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.correo_valido = False
        else:
            txt_correo.setStyleSheet("")
            self.correo_valido = True

    def verificar_contrasenia_registro(self):
        txt_contrasenia: QLineEdit = self.sender()
        contrasenia = txt_contrasenia.text()
        if not self._validar_contrasenia(contrasenia):
            print("La contraseña no cumple con las condiciones") # Para depuración
            txt_contrasenia.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.contrasenia_valida = False
        else:
            txt_contrasenia.setStyleSheet("")
            self.contrasenia_valida = True

    def verificar_contrasenia_repetida(self, contrasenia):
        txt_contrasenia_repetida: QLineEdit = self.sender()
        contrasenia_repetida = txt_contrasenia_repetida.text()
        if not contrasenia_repetida == contrasenia:
            print("Las contraseñas no son las mismas") # Para depuración
            txt_contrasenia_repetida.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            self.contrasenia_repetida_valida =  False
        else:
            txt_contrasenia_repetida.setStyleSheet("")
            self.contrasenia_repetida_valida = True

    def iniciar_sesion(self):
        txt_identificacion = self._vista.ui.txt_correo
        identificacion = txt_identificacion.text()
        txt_contrasenia =  self._vista.ui.txt_contrasenia
        contrasenia =  txt_contrasenia.text()

        if not (self._validar_correo(identificacion) or self._validar_username(identificacion)):
            print("Nombre de usuario/Correo electrónico no válido") # Para depuración
            txt_identificacion.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            return False
        elif not identificacion in self._usuarios:
            print("No se encontró ningún usuario vinculado a es nombre de usuario/correo electrónico") # Para depuración
            txt_identificacion.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            return False
        id_usuario = self._usuarios[identificacion]
        usuario = ManejadorArchivos.cargar_archivo(id_usuario, None)

        if not usuario.verificar_contrasenia(contrasenia):
            print("La contrasea no es válida, intenta de nuevo") # Para depuración
            txt_identificacion.setStyleSheet("border: 1px solid red; background-color: #ffeeee;")
            return False
        txt_identificacion.setStyleSheet("")
        print(f"Ingresó el usuario {usuario.nombre}")
        token = Token(id_usuario)
        ManejadorArchivos.guardar_archivo("token", token)
        self._vista.emitir_solicitar_mostrar_bienvenida()
        return True

    def registrarse(self):
        nombre = self._vista.ui.txt_nombre.text()
        username = self._vista.ui.txt_username.text()
        correo = self._vista.ui.txt_correo.text()
        contrasenia = self._vista.ui.txt_contrasenia.text()

        nuevo_usuario = Usuario(
            nombre=nombre,
            username=username,
            correo=correo,
            contrasenia=Usuario.hashear_contrasenia(contrasenia)
        )
        id_usuario = nuevo_usuario.id
        self._usuarios[nuevo_usuario.username] = id_usuario
        self._usuarios[nuevo_usuario.correo] = id_usuario
        ManejadorArchivos.guardar_archivo(id_usuario,nuevo_usuario)
        ManejadorArchivos.guardar_archivo("usuarios",self._usuarios)
        print("Se registró el usuario correctamente")
        self._volver_al_login()

    def _volver_al_login(self):
        self._vista.emitir_solicitar_mostrar_login()

    @staticmethod
    def _validar_correo(correo):
        regex_correo = re.compile(r'^[\w.%+-]+@[\w.-]+(\.[a-zA-Z]{2,})+$')
        return regex_correo.match(correo)

    @staticmethod
    def _validar_username(username):
        regex_username = re.compile(r'^[A-Za-z0-9_]{3,20}$')
        return regex_username.match(username)

    @staticmethod
    def _validar_contrasenia(contrasenia):
        regex_contrasenia = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z\d])[A-Za-z\d\S]{8,}$')
        return regex_contrasenia.match(contrasenia)

    @staticmethod
    def _validar_nombre(nombre):
        regex_nombre = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ' ]{2,50}$")
        return regex_nombre.match(nombre)
