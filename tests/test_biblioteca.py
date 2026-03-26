import pytest
from datetime import date

from core.biblioteca import Biblioteca
from dominio.libro import Libro
from dominio.usuario import Usuario


def test_biblioteca_registrar_libro_duplicado():
    b = Biblioteca()
    b.registrar_libro(Libro("10", "A", "X"))

    with pytest.raises(RuntimeError):
        b.registrar_libro(Libro("10", "B", "Y"))


def test_biblioteca_registrar_usuario_duplicado():
    b = Biblioteca()
    b.registrar_usuario(Usuario(1, "Ana", 3))

    with pytest.raises(RuntimeError):
        b.registrar_usuario(Usuario(1, "Otra", 3))


def test_biblioteca_prestar_libro_libro_no_encontrado():
    b = Biblioteca()
    b.registrar_usuario(Usuario(1, "Ana", 3))

    with pytest.raises(RuntimeError):
        b.prestar_libro("999", 1, date(2026, 1, 1))


def test_biblioteca_prestar_libro_usuario_no_encontrado():
    b = Biblioteca()
    b.registrar_libro(Libro("1", "T", "A"))

    with pytest.raises(RuntimeError):
        b.prestar_libro("1", 999, date(2026, 1, 1))


def test_biblioteca_prestar_libro_ya_prestado():
    b = Biblioteca()
    b.registrar_libro(Libro("1", "T", "A"))
    b.registrar_usuario(Usuario(1, "Ana", 3))
    b.registrar_usuario(Usuario(2, "Luis", 3))

    b.prestar_libro("1", 1, date(2026, 1, 1))
    with pytest.raises(RuntimeError):
        b.prestar_libro("1", 2, date(2026, 1, 2))


def test_biblioteca_prestar_libro_supera_limite():
    b = Biblioteca()
    b.registrar_usuario(Usuario(1, "Ana", 1))
    b.registrar_libro(Libro("1", "T1", "A"))
    b.registrar_libro(Libro("2", "T2", "A"))

    b.prestar_libro("1", 1, date(2026, 1, 1))
    with pytest.raises(RuntimeError):
        b.prestar_libro("2", 1, date(2026, 1, 2))


def test_biblioteca_devolver_libro_prestamo_no_encontrado():
    b = Biblioteca()
    with pytest.raises(RuntimeError):
        b.devolver_libro("1", date(2026, 1, 1))

