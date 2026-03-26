class Usuario:
    """Entidad que representa un usuario de la biblioteca."""

    def __init__(self, id_usuario, nombre: str, max_prestamos: int = 3):
        """Crea un usuario con un límite de préstamos."""
        if not isinstance(max_prestamos, int) or max_prestamos <= 0:
            raise ValueError("El numero de prestamos debe ser positivo")

        self.__id = id_usuario
        self.nombre = nombre
        self.max_prestamos = max_prestamos

    @property
    def id(self):
        return self.__id

    def __call__(self):
        return f"Usuario {self.nombre} (ID: {self.__id}) - Máx. préstamos: {self.max_prestamos}"