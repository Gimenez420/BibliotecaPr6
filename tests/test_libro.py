import pytest

from dominio.libro import Libro


def test_libro_crear_ok():
    libro = Libro("123", "El Quijote", "Cervantes")
    assert libro.isbn == "123"
    assert libro.titulo == "El Quijote"
    assert libro.autor == "Cervantes"


def test_libro_isbn_obligatorio():
    with pytest.raises(ValueError):
        Libro("", "Titulo", "Autor")


def test_libro_isbn_debe_ser_numero():
    with pytest.raises(ValueError):
        Libro("ABC", "Titulo", "Autor")


def test_libro_eq_y_hash():
    a = Libro("10", "A", "X")
    b = Libro(10, "B", "Y")
    c = Libro("11", "C", "Z")

    assert a == b
    assert a != c
    assert hash(a) == hash(b)

