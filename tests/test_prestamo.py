import pytest
from datetime import date

from dominio.libro import Libro
from dominio.prestamo import Prestamo
from dominio.usuario import Usuario


def test_prestamo_esta_activo_y_devolver():
    libro = Libro("123", "T", "A")
    usuario = Usuario(1, "Ana", 3)
    p = Prestamo(libro, usuario, date(2026, 1, 1), 7)

    assert p.esta_activo() is True
    p.devolver(date(2026, 1, 2))
    assert p.esta_activo() is False


def test_prestamo_devolver_dos_veces_da_error():
    libro = Libro("123", "T", "A")
    usuario = Usuario(1, "Ana", 3)
    p = Prestamo(libro, usuario, date(2026, 1, 1), 7)
    p.devolver(date(2026, 1, 2))

    with pytest.raises(RuntimeError):
        p.devolver(date(2026, 1, 3))


def test_prestamo_esta_vencido():
    libro = Libro("123", "T", "A")
    usuario = Usuario(1, "Ana", 3)
    p = Prestamo(libro, usuario, date(2026, 1, 1), 7)

    assert p.esta_vencido(date(2026, 1, 8)) is False
    assert p.esta_vencido(date(2026, 1, 9)) is True

