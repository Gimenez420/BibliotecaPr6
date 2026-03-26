import pytest

from dominio.usuario import Usuario


def test_usuario_crear_ok():
    u = Usuario(1, "Ana", 3)
    assert u.id == 1
    assert u.nombre == "Ana"
    assert u.max_prestamos == 3


@pytest.mark.parametrize("max_prestamos", [0, -1, "3"])
def test_usuario_max_prestamos_debe_ser_positivo(max_prestamos):
    with pytest.raises(ValueError):
        Usuario(1, "Ana", max_prestamos)


def test_usuario_call_devuelve_texto():
    u = Usuario(7, "Pepe", 2)
    texto = u()
    assert "Pepe" in texto
    assert "7" in texto

