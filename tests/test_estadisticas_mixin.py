from datetime import date

from core.biblioteca import Biblioteca
from dominio.libro import Libro
from dominio.usuario import Usuario


def test_estadisticas_mixin_total_libros_y_prestamos():
    b = Biblioteca()
    assert b.total_libros() == 0
    assert b.total_usuarios() == 0
    assert b.total_prestamos() == 0

    b.registrar_libro(Libro("1", "T", "A"))
    b.registrar_usuario(Usuario(1, "Ana", 3))
    b.prestar_libro("1", 1, date(2026, 1, 1))

    assert b.total_libros() == 1
    assert b.total_usuarios() == 1
    assert b.total_prestamos() == 1

