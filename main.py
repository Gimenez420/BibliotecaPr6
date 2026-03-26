"""Interfaz por consola del sistema de biblioteca.

Este archivo contiene el menú y las funciones de interacción con el usuario
para llamar a la lógica de `Biblioteca`.
"""

import os
from datetime import date, timedelta

from core.biblioteca import Biblioteca
from dominio.libro import Libro
from dominio.usuario import Usuario


def limpiar_pantalla():
    """Limpia la consola (Windows)."""
    os.system("cls")

def mostrar_menu():
    """Muestra el menú principal por consola."""
    print("\n==============================")
    print(" SISTEMA DE BIBLIOTECA DIGITAL")
    print("==============================")
    print("1. Registrar libro")
    print("2. Registrar usuario")
    print("3. Listar usuarios")
    print("4. Prestar libro")
    print("5. Devolver libro")
    print("6. Consultar préstamos activos")
    print("7. Consultar préstamos vencidos")
    print("8. Ver histórico de préstamos")
    print("9. Buscar libro")
    print("10. Listar libros")
    print("11. Exportar CSV")
    print("12. Exportar JSON")
    print("13. Importar CSV")
    print("14. Importar JSON")
    print("15. Mostrar estadísticas")
    print("0 Salir")

def pedir_fecha(mensaje):
    """Pide una fecha en formato ISO (YYYY-MM-DD)."""
    fecha_str = input(mensaje).strip()
    return date.fromisoformat(fecha_str)

def registrar_libro(biblioteca):
    """Solicita datos por consola y registra un libro."""
    limpiar_pantalla()
    isbn = input("ISBN: ").strip()

    limpiar_pantalla()
    titulo = input("Título: ").strip()

    limpiar_pantalla()
    autor = input("Autor: ").strip()

    try:
        libro = Libro(isbn, titulo, autor)
        biblioteca.registrar_libro(libro)
    except Exception as e:
        print(f"No es posible registrar el libro: {e}")
        input("\nPulse Enter para continuar...")
        return

    limpiar_pantalla()

    print("Libro registrado correctamente.")
    input("\nPulse Enter para continuar...")


def registrar_usuario(biblioteca):
    """Solicita datos por consola y registra un usuario."""
    limpiar_pantalla()
    id_usuario = input("ID del usuario: ").strip()

    if not id_usuario.isdigit():
        print("El ID debe ser numérico")
        input("\nPulse Enter para continuar...")
        return

    limpiar_pantalla()
    nombre = input("Nombre: ").strip()

    limpiar_pantalla()
    max_prestamos = input("Máximo de préstamos: ").strip()

    if not max_prestamos.isdigit():
        print("Debe ser un número")
        input("\nPulse Enter para continuar...")
        return

    limpiar_pantalla()
    try:
        usuario = Usuario(int(id_usuario), nombre, int(max_prestamos))
        biblioteca.registrar_usuario(usuario)
    except Exception as e:
        print(f"No es posible registrar el usuario: {e}")
        input("\nPulse Enter para continuar...")
        return

    print("Usuario registrado correctamente.")
    input("\nPulse Enter para continuar...")


def prestar_libro(biblioteca):
    """Realiza un préstamo solicitando datos por consola."""
    limpiar_pantalla()
    isbn = input("ISBN del libro: ").strip()

    limpiar_pantalla()
    id_usuario = input("ID del usuario: ").strip()

    if not id_usuario.isdigit():
        print("El ID debe ser numérico")
        input("\nPulse Enter para continuar...")
        return

    limpiar_pantalla()
    try:
        fecha = pedir_fecha("Fecha del préstamo (YYYY-MM-DD): ")
        prestamo = biblioteca.prestar_libro(isbn, int(id_usuario), fecha)
    except Exception as e:
        print(f"No es posible realizar el préstamo: {e}")
        input("\nPulsa Enter para continuar...")
        return

    print(
        f"Préstamo realizado: {prestamo.libro.titulo} → {prestamo.usuario.nombre}"
    )
    input("\nPulsa Enter para continuar...")


def devolver_libro(biblioteca):
    """Devuelve un libro y muestra la multa si aplica."""
    limpiar_pantalla()
    isbn = input("ISBN del libro a devolver: ").strip()

    limpiar_pantalla()
    try:
        fecha = pedir_fecha("Fecha de devolución (YYYY-MM-DD): ")
        prestamo = biblioteca.devolver_libro(isbn, fecha)
    except Exception as e:
        print(f"No es posible devolver el libro: {e}")
        input("\nPulse Enter para continuar...")
        return

    multa = biblioteca.politica_multa.calcular(prestamo, fecha)
    limpiar_pantalla()
    print(
        f"Libro devuelto: {prestamo.libro.titulo} "
        f"por {prestamo.usuario.nombre}"
    )

    if multa > 0:
        print(f"Multa por retraso: {multa} €")
    else:
        print("Devolución realizada a tiempo (sin multa).")

    input("\nPulse Enter para continuar...")


def mostrar_tabla_prestamos(prestamos, titulo):
    """Muestra una lista de préstamos formateada."""
    limpiar_pantalla()

    if not prestamos:
        print(f"No hay préstamos para mostrar: {titulo}")
        input("\nPulsa Enter...")
        return

    print(f"\n{titulo.upper()}\n")

    print(
        f"{'ISBN':<15} {'LIBRO':<25} {'USUARIO':<20} "
        f"{'ESTADO':<10} {'F. LÍMITE':<12}"
    )
    print("-" * 90)

    for p in prestamos:
        estado = "Activo" if p.esta_activo() else "Devuelto"
        fecha_limite = p.fecha_inicio + timedelta(days=p.dias_maximos)

        print(
            f"{p.libro.isbn:<15} "
            f"{p.libro.titulo:<25} "
            f"{p.usuario.nombre:<20} "
            f"{estado:<10} "
            f"{fecha_limite}"
        )

    input("\nPulsa Enter para continuar...")

def consultar_prestamos_activos(biblioteca):
    """Muestra los préstamos que aún no han sido devueltos."""
    prestamos = [p for p in biblioteca.prestamos if p.esta_activo()]
    mostrar_tabla_prestamos(prestamos, "Préstamos Activos")


def consultar_prestamos_vencidos(biblioteca):
    """Muestra los préstamos activos cuya fecha límite ha pasado."""
    hoy = date.today()
    prestamos = [
        p for p in biblioteca.prestamos
        if p.esta_activo() and p.esta_vencido(hoy)
    ]
    mostrar_tabla_prestamos(prestamos, "Préstamos Vencidos")


def ver_historico_prestamos(biblioteca):
    """Muestra el historial completo de préstamos (activos y devueltos)."""
    mostrar_tabla_prestamos(biblioteca.prestamos, "Histórico Completo de Préstamos")


def buscar_libro(biblioteca):
    """Busca libros por título o autor."""
    limpiar_pantalla()

    texto = input("Título o autor a buscar: ").lower()

    resultados = [
        libro for libro in biblioteca.libros
        if texto in libro.titulo.lower() or texto in libro.autor.lower()
    ]

    limpiar_pantalla()

    if not resultados:
        print("No se encontraron resultados.")
        input("\nPulsa Enter para continuar...")
        return

    print("\nRESULTADOS DE LA BÚSQUEDA\n")

    print(f"{'ISBN':<15} {'TÍTULO':<30} {'AUTOR':<25}")
    print("-" * 70)

    for libro in resultados:
        print(f"{libro.isbn:<15} {libro.titulo:<30} {libro.autor:<25}")

    print(f"\nTotal encontrados: {len(resultados)}")
    input("\nPulsa Enter para continuar...")


def listar_usuarios(biblioteca):
    """Lista usuarios registrados."""
    limpiar_pantalla()

    if not biblioteca.usuarios:
        print("No hay usuarios registrados.")
        input("\nPulsa Enter para continuar...")
        return

    print("\nUSUARIOS REGISTRADOS\n")

    print(f"{'ID':<10} {'NOMBRE':<25} {'MÁX. PRÉSTAMOS':<18}")
    print("-" * 55)

    for usuario in biblioteca.usuarios:
        print(f"{usuario.id:<10} {usuario.nombre:<25} {usuario.max_prestamos:<18}")

    print(f"\nTotal usuarios: {len(biblioteca.usuarios)}")
    input("\nPulsa Enter para continuar...")

def exportar_todo_csv(biblioteca):
    """Exporta el estado a CSV."""
    limpiar_pantalla()
    print("Introduzca el nombre de la carpeta donde se guardaran los archivos")
    ruta = input()

    limpiar_pantalla()
    biblioteca.exportar_todo_csv(ruta + ".csv")
    print("Archivos exportados correctamente")
    input("\nPulse Enter para continuar...")


def exportar_todo_json(biblioteca):
    """Exporta el estado a JSON."""
    limpiar_pantalla()
    print("Introduzca el nombre del archivo")
    ruta = input()

    limpiar_pantalla()
    biblioteca.exportar_todo_json(ruta + ".json")
    print("Archivo exportado correctamente")

    input("\nPulse Enter para continuar...")


def importar_todo_csv(biblioteca):
    """Importa el estado desde CSV."""
    limpiar_pantalla()
    print("Introduzca el nombre de la carpeta contenedora de los archivos a importar")
    ruta = input()

    limpiar_pantalla()
    print("Archivos importados")
    biblioteca.importar_todo_csv(ruta + ".csv")

    input("\nPulse Enter para continuar....")

def importar_todo_json(biblioteca):
    """Importa el estado desde JSON."""
    limpiar_pantalla()
    print("Intrtoduzca el nombre del archivo a importar")
    ruta = input()

    limpiar_pantalla()
    print("Archivo importado")
    biblioteca.importar_todo_json(ruta + ".json")

    input("\nPulse Enter para continuar...")


def listar_libros(biblioteca):
    """Lista libros disponibles."""
    limpiar_pantalla()

    if not biblioteca.libros:
        print("No hay libros registrados.")
        input("\nPulsa Enter...")
        return

    print("\nLIBROS DISPONIBLES\n")
    print(f"{'ISBN':<15} {'TÍTULO':<30} {'AUTOR':<25}")
    print("-" * 70)

    for libro in biblioteca:
        print(f"{libro.isbn:<15} {libro.titulo:<30} {libro.autor:<25}")

    input("\nPulsa Enter para continuar...")


def mostrar_estadisticas(biblioteca):
    """Muestra estadísticas básicas de la biblioteca."""
    limpiar_pantalla()

    total_libros = biblioteca.total_libros()
    total_usuarios = biblioteca.total_usuarios()
    total_prestamos = biblioteca.total_prestamos()

    print("\nESTADÍSTICAS\n")
    print(f"- Total de libros: {total_libros}")
    print(f"- Total de usuarios: {total_usuarios}")
    print(f"- Total de préstamos: {total_prestamos}")

    input("\nPulsa Enter para continuar...")


def main():
    """Bucle principal del programa."""
    biblioteca = Biblioteca()


    while True:
        limpiar_pantalla()
        mostrar_menu()

        opcion = input("Seleccione una opción: ").strip()

        try:

            if opcion == "1":
                registrar_libro(biblioteca)

            elif opcion == "2":
                registrar_usuario(biblioteca)

            elif opcion == "3":
                listar_usuarios(biblioteca)

            elif opcion == "4":
                prestar_libro(biblioteca)

            elif opcion == "5":
                devolver_libro(biblioteca)

            elif opcion == "6":
                consultar_prestamos_activos(biblioteca)

            elif opcion == "7":
                consultar_prestamos_vencidos(biblioteca)

            elif opcion == "8":
                ver_historico_prestamos(biblioteca)

            elif opcion == "9":
                buscar_libro(biblioteca)

            elif opcion == "10":
                listar_libros(biblioteca)

            elif opcion == "11":
                exportar_todo_csv(biblioteca)

            elif opcion == "12":
                exportar_todo_json(biblioteca)

            elif opcion == "13":
                importar_todo_csv(biblioteca)

            elif opcion == "14":
                importar_todo_json(biblioteca)

            elif opcion == "15":
                mostrar_estadisticas(biblioteca)

            elif opcion == "0":
                limpiar_pantalla()
                break
            else:
                print("Opción no válida.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
