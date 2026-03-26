"""Servicios relacionados con multas por retraso en devoluciones."""

from abc import ABC, abstractmethod
from datetime import timedelta

class PoliticaMulta(ABC):
    """Interfaz de política de multa."""

    @abstractmethod
    def calcular(self, prestamo, fecha):
        pass


class MultaPorDia(PoliticaMulta):
    """Calcula una multa fija por cada día de retraso."""

    def __init__(self, importe):
        self.importe = importe

    def calcular(self, prestamo, fecha):
        fecha_limite = prestamo.fecha_inicio + timedelta(days=prestamo.dias_maximos)

        if fecha <= fecha_limite:
            return 0

        dias = (fecha - fecha_limite).days

        return dias * self.importe