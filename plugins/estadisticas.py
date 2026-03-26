class EstadisticasMixin:
    """Mixin con estadísticas básicas.

    Se espera que la clase que herede tenga atributos `libros`, `usuarios` y
    `prestamos`.
    """

    def total_libros(self):
        """Devuelve el número total de libros registrados."""
        return len(self.libros)

    def total_usuarios(self):
        """Devuelve el número total de usuarios registrados."""
        return len(self.usuarios)

    def total_prestamos(self):
        """Devuelve el número total de préstamos registrados."""
        return len(self.prestamos)