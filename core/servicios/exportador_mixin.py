from datetime import date

"""Funciones de importación/exportación para el estado de la biblioteca.

Se implementa como mixin para que la clase `Biblioteca` herede estos métodos.
"""

import csv
import json
import os

from dominio.libro import Libro
from dominio.prestamo import Prestamo
from dominio.usuario import Usuario

class ExportadorMixin:
    """Mixin con utilidades de exportación/importación (CSV/JSON)."""

    def importar_todo_json(self, ruta):
        """Importa libros, usuarios y préstamos desde un archivo JSON."""
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)

        # Limpiar estado actual (opcional)
        self.libros = []
        self.usuarios = []
        self.prestamos = []

        # Libros
        for l in datos["libros"]:
            libro = Libro(l["isbn"], l["titulo"], l["autor"])
            self.libros.append(libro)

        # Usuarios
        for u in datos["usuarios"]:
            id_usuario = u["id"]
            try:
                id_usuario = int(id_usuario)
            except (ValueError, TypeError):
                pass

            usuario = Usuario(id_usuario, u["nombre"], u["max_prestamos"])
            self.usuarios.append(usuario)

        # Diccionarios para reconstrucción
        libros_dict = {l.isbn: l for l in self.libros}
        usuarios_dict = {u.id: u for u in self.usuarios}

        # Préstamos
        for p in datos["prestamos"]:
            libro = libros_dict[p["isbn"]]
            id_usuario = p["id_usuario"]
            try:
                id_usuario = int(id_usuario)
            except (ValueError, TypeError):
                pass

            usuario = usuarios_dict[id_usuario]

            prestamo = Prestamo(
                libro,
                usuario,
                date.fromisoformat(p["fecha_inicio"]),
                p["dias_maximos"],
            )

            if p["fecha_devolucion"]:
                prestamo.fecha_devolucion = date.fromisoformat(p["fecha_devolucion"])

            self.prestamos.append(prestamo)

    def exportar_todo_json(self, ruta):
        """Exporta libros, usuarios y préstamos a un archivo JSON."""
        datos = {
            "libros": [
                {
                    "isbn": l.isbn,
                    "titulo": l.titulo,
                    "autor": l.autor
                }
                for l in self.libros
            ],
            "usuarios": [
                {
                    "id": u.id,
                    "nombre": u.nombre,
                    "max_prestamos": u.max_prestamos
                }
                for u in self.usuarios
            ],
            "prestamos": [
                {
                    "isbn": p.libro.isbn,
                    "id_usuario": p.usuario.id,
                    "fecha_inicio": p.fecha_inicio.isoformat(),
                    "fecha_devolucion": p.fecha_devolucion.isoformat() if p.fecha_devolucion else None,
                    "dias_maximos": p.dias_maximos
                }
                for p in self.prestamos
            ]
        }

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)

    def exportar_todo_csv(self, carpeta):
        """Exporta libros, usuarios y préstamos a CSV (tres ficheros)."""
        os.makedirs(carpeta, exist_ok=True)

        # LIBROS
        with open(
            os.path.join(carpeta, "libros.csv"),
            "w",
            newline="",
            encoding="utf-8",
        ) as f:
            writer = csv.writer(f)
            writer.writerow(["isbn", "titulo", "autor"])
            for l in self.libros:
                writer.writerow([l.isbn, l.titulo, l.autor])

        # USUARIOS
        with open(
            os.path.join(carpeta, "usuarios.csv"),
            "w",
            newline="",
            encoding="utf-8",
        ) as f:
            writer = csv.writer(f)
            writer.writerow(["id", "nombre", "max_prestamos"])
            for u in self.usuarios:
                writer.writerow([u.id, u.nombre, u.max_prestamos])

        # PRÉSTAMOS
        with open(
            os.path.join(carpeta, "prestamos.csv"),
            "w",
            newline="",
            encoding="utf-8",
        ) as f:
            writer = csv.writer(f)
            writer.writerow(["isbn", "id_usuario", "fecha_inicio", "fecha_devolucion", "dias_maximos"])
            for p in self.prestamos:
                writer.writerow([
                    p.libro.isbn,
                    p.usuario.id,
                    p.fecha_inicio.isoformat(),
                    p.fecha_devolucion.isoformat() if p.fecha_devolucion else "",
                    p.dias_maximos
                ])

    def importar_todo_csv(self, carpeta):
        """Importa libros, usuarios y préstamos desde CSV (tres ficheros)."""
        # Limpiar estado
        self.libros = []
        self.usuarios = []
        self.prestamos = []

        # LIBROS
        with open(os.path.join(carpeta, "libros.csv"), "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for fila in reader:
                libro = Libro(fila["isbn"], fila["titulo"], fila["autor"])
                self.libros.append(libro)

        # USUARIOS
        with open(os.path.join(carpeta, "usuarios.csv"), "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for fila in reader:
                id_usuario = fila["id"]
                try:
                    id_usuario = int(id_usuario)
                except (ValueError, TypeError):
                    pass

                usuario = Usuario(
                    id_usuario,
                    fila["nombre"],
                    int(fila["max_prestamos"])
                )
                self.usuarios.append(usuario)

        # Diccionarios para reconstrucción
        libros_dict = {l.isbn: l for l in self.libros}
        usuarios_dict = {u.id: u for u in self.usuarios}

        # PRÉSTAMOS
        with open(os.path.join(carpeta, "prestamos.csv"), "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for fila in reader:
                libro = libros_dict[fila["isbn"]]
                id_usuario = fila["id_usuario"]
                try:
                    id_usuario = int(id_usuario)
                except (ValueError, TypeError):
                    pass

                usuario = usuarios_dict[id_usuario]

                prestamo = Prestamo(
                    libro,
                    usuario,
                    date.fromisoformat(fila["fecha_inicio"]),
                    int(fila["dias_maximos"])
                )

                if fila["fecha_devolucion"]:
                    prestamo.fecha_devolucion = date.fromisoformat(fila["fecha_devolucion"])

                self.prestamos.append(prestamo)