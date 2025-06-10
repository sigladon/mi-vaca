from datetime import date


class Transaccion:
    def __init__(self, tipo, monto, descripcion, categoria, fecha: date, notas=""):
        self.tipo = tipo
        self.monto = monto
        self.descripcion = descripcion
        self.categoria = categoria
        self.fecha = fecha
        self.notas = notas