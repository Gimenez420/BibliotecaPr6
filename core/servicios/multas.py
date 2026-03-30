"""Servicios relacionados con multas por retraso en devoluciones."""


from datetime import timedelta
class MetaMulta(type):

    def __new__(cls, nombre, bases, diccionario):
        if nombre != "PoliticaMulta":
            if "calcular" not in diccionario:
                raise TypeError(f"{nombre} debe implementar 'calcular'")
        return super().__new__(cls, nombre, bases, diccionario)
    

class PoliticaMulta(metaclass=MetaMulta):
    """Interfaz de política de multa."""

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
    

class MultaAcumulativa(PoliticaMulta):
    """Multa donde cada día suma su número (1 + 2 + ... + n)."""

    def calcular(self, prestamo, fecha):
        fecha_limite = prestamo.fecha_inicio + timedelta(days=prestamo.dias_maximos)

        if fecha <= fecha_limite:
            return 0

        dias = (fecha - fecha_limite).days

        # Fórmula de suma acumulada
        return dias * (dias + 1) // 2