import os
import pickle


class ManejadorArchivos:

    @staticmethod
    def cargar_archivo(nombre_archivo, objeto_por_defecto):
        ruta_archivo = f"./datos/{nombre_archivo}.dat"
        try:
            with open(ruta_archivo, "rb") as file:
                return pickle.load(file)
        except (EOFError, FileNotFoundError):
            return objeto_por_defecto

    @staticmethod
    def guardar_archivo(nombre_archivo, objeto_a_guardar):
        ruta_archivo = f"./datos/{nombre_archivo}.dat"
        with open(ruta_archivo, "wb") as file:
            pickle.dump(objeto_a_guardar, file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def borrar_archivo(nombre_archivo):
        ruta_archivo = f"./datos/{nombre_archivo}.dat"
        try:
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
                print(f"Archivo '{nombre_archivo}' borrado exitosamente.")
            else:
                print(f"El archivo '{nombre_archivo}' no existe.")
        except OSError as e:
            print(f"Error al intentar borrar el archivo '{nombre_archivo}': {e}")
