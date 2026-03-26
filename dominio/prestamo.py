from datetime import date, timedelta


class Prestamo:
    """Entidad que representa un préstamo de un libro a un usuario."""

    def __init__(self, libro, usuario, fecha_inicio: date, dias_maximos: int = 7):
        """Crea un préstamo con fecha de inicio y duración máxima."""
        self.libro = libro
        self.usuario = usuario
        self.fecha_inicio = fecha_inicio
        self.dias_maximos = dias_maximos
        self.fecha_devolucion = None

    def esta_activo(self):
        """Devuelve True si el préstamo todavía no se ha devuelto."""
        return self.fecha_devolucion is None

    def esta_vencido(self, fecha_actual: date):
        """Devuelve True si el préstamo está vencido en `fecha_actual`."""
        fecha_limite = self.fecha_inicio + timedelta(days=self.dias_maximos)
        return fecha_actual > fecha_limite

    def devolver(self, fecha: date):
        """Marca el préstamo como devuelto en la fecha indicada."""
        if not self.esta_activo():
            raise RuntimeError("El préstamo ya fue devuelto")
        self.fecha_devolucion = fecha

