from datetime import date

from core.biblioteca import Biblioteca
from core.servicios.multas import MultaPorDia
from dominio.libro import Libro
from dominio.usuario import Usuario


def test_multa_por_dia():
    biblioteca = Biblioteca()
    biblioteca.politica_multa = MultaPorDia(2)

    libro = Libro("1", "T", "A")
    usuario = Usuario(1, "Ana", 3)
    biblioteca.registrar_libro(libro)
    biblioteca.registrar_usuario(usuario)

    prestamo = biblioteca.prestar_libro("1", 1, date(2026, 1, 1))

    multa = biblioteca.politica_multa.calcular(prestamo, date(2026, 1, 7))
    assert multa == 0

    multa = biblioteca.politica_multa.calcular(prestamo, date(2026, 1, 10))
    assert multa == 4

