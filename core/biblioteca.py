"""Lógica principal de la biblioteca (alta, préstamos y devoluciones)."""

from datetime import date

from core.servicios.exportador_mixin import ExportadorMixin
from core.servicios.validaciones import valodar_campos
from dominio.libro import Libro
from dominio.prestamo import Prestamo
from dominio.usuario import Usuario
from plugins.estadisticas import EstadisticasMixin

from .servicios.multas import MultaPorDia


class Biblioteca(ExportadorMixin, EstadisticasMixin):
    """Representa una biblioteca en memoria.

    Guarda listas de libros, usuarios y préstamos, y expone operaciones típicas:
    registrar, prestar y devolver.
    """

    def __init__(self):
        # Estado principal del sistema
        self.libros = []  # libros registrados
        self.usuarios = []  # usuarios dados de alta
        self.prestamos = []  # historial de préstamos

        # Política de multa configurable
        self.politica_multa = MultaPorDia(1)

    @valodar_campos()
    def registrar_libro(self, libro: Libro):
        """Registra un libro en la biblioteca."""
        if not isinstance(libro, Libro):
            raise TypeError("El objeto a registrar debe ser una instancia de Libro")

        if any(l.isbn == libro.isbn for l in self.libros):
            raise RuntimeError("Ya existe un libro con el mismo ISBN")

        self.libros.append(libro)

    @valodar_campos()
    def registrar_usuario(self, usuario: Usuario):
        """Registra un usuario en la biblioteca."""
        if not isinstance(usuario, Usuario):
            raise TypeError("El objeto a registrar debe ser una instancia de Usuario")

        if any(u.id == usuario.id for u in self.usuarios):
            raise RuntimeError("Ya existe un usuario con la misma ID")

        self.usuarios.append(usuario)

    @valodar_campos()
    def prestar_libro(self, isbn: str, id_usuario, fecha: date):
        """Crea un préstamo si se cumplen las condiciones."""
        if not isinstance(isbn, str) or not isbn:
            raise ValueError("El ISBN debe ser una cadena no vacía")
        if not isinstance(id_usuario, (str, int)) or (
            isinstance(id_usuario, str) and not id_usuario
        ):
            raise ValueError("El ID de usuario debe ser una cadena no vacía o un entero")
        if not isinstance(fecha, date):
            raise TypeError("La fecha debe ser una instancia de datetime.date")

        libro = next((l for l in self.libros if l.isbn == isbn), None)
        if libro is None:
            raise RuntimeError("Libro no encontrado")

        usuario = next((u for u in self.usuarios if u.id == id_usuario), None)
        if usuario is None:
            raise RuntimeError("Usuario no encontrado")

        if any(p.libro == libro and p.esta_activo() for p in self.prestamos):
            raise RuntimeError("Libro ya prestado")

        prestamos_activos = sum(
            1 for p in self.prestamos if p.usuario == usuario and p.esta_activo()
        )
        if prestamos_activos >= usuario.max_prestamos:
            raise RuntimeError("Usuario supera límite de préstamos")

        prestamo = Prestamo(libro, usuario, fecha)
        self.prestamos.append(prestamo)
        return prestamo

    @valodar_campos()
    def devolver_libro(self, isbn: str, fecha: date):
        """Devuelve un libro y calcula la multa si aplica."""
        if not isinstance(isbn, str) or not isbn:
            raise ValueError("El ISBN debe ser una cadena no vacía")
        if not isinstance(fecha, date):
            raise TypeError("La fecha debe ser una instancia de datetime.date")

        prestamo = next(
            (p for p in self.prestamos if p.libro.isbn == isbn and p.esta_activo()),
            None,
        )
        if prestamo is None:
            raise RuntimeError("Préstamo no encontrado o ya devuelto")

        prestamo.devolver(fecha)

        multa = self.politica_multa.calcular(prestamo, fecha)
        if multa > 0:
            print(f"¡Multa aplicada! Importe: {multa}€")

        return prestamo

    def __iter__(self):
        """Permite iterar directamente sobre los libros."""
        return iter(self.libros)

    def __getitem__(self, index):
        """Acceso por índice a la lista de libros."""
        return self.libros[index]

    def __add__(self, libro: Libro):
        """Permite usar `biblioteca + libro` para crear una nueva biblioteca."""
        if not isinstance(libro, Libro):
            return NotImplemented

        nueva_biblioteca = Biblioteca()
        nueva_biblioteca.libros = self.libros + [libro]
        nueva_biblioteca.usuarios = self.usuarios
        nueva_biblioteca.prestamos = self.prestamos
        return nueva_biblioteca