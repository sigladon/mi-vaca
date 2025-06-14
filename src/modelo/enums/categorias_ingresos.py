from enum import Enum
from src.modelo.entidades.categoria import Categoria

class CategoriasIngresos(Enum):
    SALARIO = Categoria(
        200, "Salario",
        "Ingresos regulares recibidos de un empleador por trabajo."
    )
    TRABAJO_INDEPENDIENTE = Categoria(
        201, "Trabajo Independiente",
        "Ingresos generados por servicios profesionales, consultorías o proyectos freelance."
    )
    INVERSIONES = Categoria(
        202, "Inversiones",
        "Ganancias de inversiones como dividendos, intereses, alquileres o venta de activos."
    )
    VENTAS = Categoria(
        203, "Ventas",
        "Ingresos por la venta de bienes o servicios (no relacionados con un negocio principal)."
    )
    REGALOS = Categoria(
        204, "Regalos",
        "Dinero recibido como obsequio de familiares o amigos."
    )
    REEMBOLSOS = Categoria(
        205, "Reembolsos",
        "Dinero devuelto por gastos previamente incurridos (ej. devoluciones de compras, seguros)."
    )
    OTROS = Categoria(
        206, "Otros",
        "Cualquier otro tipo de ingreso no categorizado anteriormente."
    )
