from datetime import timedelta
from dateutil.relativedelta import relativedelta
from enum import Enum


class TipoFrecuencia(Enum):
    DIA = relativedelta(days=1)
    SEMANA = relativedelta(days=7)
    MES = relativedelta(month=1)
    ANIO = relativedelta(year=1)
