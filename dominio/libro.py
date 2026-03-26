class Libro:
    """Entidad que representa un libro."""

    def __init__(self, isbn, titulo: str, autor: str):
        """Crea un libro validando el ISBN."""
        if not isbn:
            raise ValueError("El ISBN es obligatorio")

        try:
            valor_int = int(isbn)
        except (ValueError, TypeError):
            raise ValueError("El ISBN debe ser un número")

        self._isbn = valor_int
        self.titulo = titulo
        self.autor = autor

    @property
    def isbn(self):
        """Devuelve el ISBN como cadena."""
        return str(self._isbn)

    def __str__(self):
        return f"{self.titulo} - {self.autor} (ISBN: {self.isbn})"

    def __repr__(self):
        return f"Libro(isbn={self.isbn}, titulo='{self.titulo}', autor='{self.autor}')"

    def __eq__(self, other):
        if not isinstance(other, Libro):
            return NotImplemented
        return self._isbn == other._isbn

    def __hash__(self):
        return hash(self._isbn)