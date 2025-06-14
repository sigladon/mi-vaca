from enum import Enum
from src.modelo.entidades.categoria import Categoria

class CategoriasGastos(Enum):
    VIVIENDA = Categoria(
        100, "Vivienda",
        "Gastos relacionados con el hogar: alquiler/hipoteca, reparaciones, mantenimiento."
    )
    SERVICIOS_BASICOS = Categoria(
        101, "Servicios Básicos",
        "Gastos esenciales como electricidad, agua, gas, internet y teléfono."
    )
    TRANSPORTE = Categoria(
        102, "Transporte",
        "Gastos de movilidad: combustible, transporte público, mantenimiento del vehículo, taxis."
    )
    EDUCACION = Categoria(
        103, "Educación",
        "Gastos de formación académica: matrículas, útiles escolares, libros, cursos."
    )
    SALUD = Categoria(
        104, "Salud",
        "Gastos médicos: consultas, medicamentos, seguros de salud, tratamientos."
    )
    SUSCRIPCIONES = Categoria(
        105, "Suscripciones",
        "Pagos recurrentes por servicios digitales o físicos: streaming, gimnasio, software."
    )
    DEUDAS = Categoria(
        106, "Deudas",
        "Pagos de préstamos personales, tarjetas de crédito, u otras obligaciones financieras."
    )
    ALIMENTACION = Categoria(
        107, "Alimentación",
        "Gastos de supermercado, restaurantes, y comida a domicilio."
    )
    ENTRETENIMIENTO = Categoria(
        108, "Entretenimiento",
        "Gastos de ocio: cine, conciertos, hobbies, salidas."
    )
    ROPA = Categoria(
        109, "Ropa",
        "Gastos en vestimenta y calzado."
    )
    HOGAR = Categoria(
        110, "Hogar",
        "Gastos en artículos para el hogar: limpieza, decoración, pequeños electrodomésticos."
    )
    VIAJES = Categoria(
        111, "Viajes",
        "Gastos relacionados con viajes: alojamiento, transporte, actividades turísticas."
    )
    MASCOTAS = Categoria(
        112, "Mascotas",
        "Gastos para animales domésticos: comida, veterinario, accesorios."
    )
    OTROS = Categoria(
        113, "Otros",
        "Gastos no categorizados previamente o de carácter esporádico."
    )
