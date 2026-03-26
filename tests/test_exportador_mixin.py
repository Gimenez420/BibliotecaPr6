import json
from datetime import date

from core.biblioteca import Biblioteca
from dominio.libro import Libro
from dominio.usuario import Usuario


def test_exportador_mixin_export_import_json(tmp_path):
    b1 = Biblioteca()
    b1.registrar_libro(Libro("1", "T", "A"))
    b1.registrar_usuario(Usuario(1, "Ana", 2))
    b1.prestar_libro("1", 1, date(2026, 1, 1))

    ruta = tmp_path / "estado.json"
    b1.exportar_todo_json(str(ruta))

    datos = json.loads(ruta.read_text(encoding="utf-8"))
    assert "libros" in datos
    assert "usuarios" in datos
    assert "prestamos" in datos

    b2 = Biblioteca()
    b2.importar_todo_json(str(ruta))

    assert len(b2.libros) == 1
    assert len(b2.usuarios) == 1
    assert len(b2.prestamos) == 1
    assert isinstance(b2.usuarios[0].id, int)


def test_exportador_mixin_export_import_csv(tmp_path):
    b1 = Biblioteca()
    b1.registrar_libro(Libro("1", "T", "A"))
    b1.registrar_usuario(Usuario(1, "Ana", 2))
    b1.prestar_libro("1", 1, date(2026, 1, 1))

    carpeta = tmp_path / "estado_csv"
    b1.exportar_todo_csv(str(carpeta))

    assert (carpeta / "libros.csv").exists()
    assert (carpeta / "usuarios.csv").exists()
    assert (carpeta / "prestamos.csv").exists()

    b2 = Biblioteca()
    b2.importar_todo_csv(str(carpeta))

    assert len(b2.libros) == 1
    assert len(b2.usuarios) == 1
    assert len(b2.prestamos) == 1
    assert isinstance(b2.usuarios[0].id, int)

