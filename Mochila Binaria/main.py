# main.py

from lector_archivo import leer_datos
from heuristicas.mayor_costo import heuristica_mayor_costo

METAHEURISTICAS = {
    "Constructivas": [
        "Mayor costo",
        "Menor volumen",
        "Mayor combinación lineal de factores",
        "Mayor costo/volumen",
        "Azar",
        "Alternancia",
        "Menor capacidad residual libre"
    ],
    "De reducción": [
        "Menor costo",
        "Mayor volumen",
        "Menor combinación lineal de factores",
        "Menor costo/volumen",
        "Azar",
        "Alternancia"
    ],
    "De descomposición": [
        "Dividir en submochilas"
    ]
}


def mostrar_menu_principal():
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Cargar datos de productos")
    print("2. Configurar y ejecutar metaheurística")
    print("3. Salir")


def seleccionar_tipo_metaheuristica():
    print("\nTipos de Metaheurísticas disponibles:")
    for i, tipo in enumerate(METAHEURISTICAS.keys(), start=1):
        print(f"{i}. {tipo}")

    while True:
        try:
            opcion = int(input("Seleccione el tipo de metaheurística: "))
            tipos = list(METAHEURISTICAS.keys())
            if 1 <= opcion <= len(tipos):
                return tipos[opcion - 1]
            else:
                print("Opción inválida.")
        except ValueError:
            print("Ingrese un número válido.")


def seleccionar_heuristicas(tipo):
    heuristicas = METAHEURISTICAS[tipo]
    print(f"\nHeurísticas disponibles para {tipo}:")
    for i, h in enumerate(heuristicas, start=1):
        print(f"{i}. {h}")

    print("\nPuede seleccionar varias heurísticas separadas por comas (ej: 1,3)")
    seleccion = input("Seleccione heurísticas: ")

    seleccionadas = []
    try:
        indices = [int(x.strip()) for x in seleccion.split(',')]
        for i in indices:
            if 1 <= i <= len(heuristicas):
                seleccionadas.append(heuristicas[i - 1])
    except ValueError:
        print("Entrada inválida.")

    return seleccionadas


def ejecutar_heuristica(nombre_heuristica, productos, capacidad):
    """Ejecuta la heurística correspondiente según el nombre."""
    print(f"\nEjecutando heurística: {nombre_heuristica}")

    if nombre_heuristica.lower() == "mayor costo":
        heuristica_mayor_costo(productos, capacidad)
    else:
        print(f"La heurística '{nombre_heuristica}' aún no está implementada.")


def main():
    productos = []
    capacidad = None

    while True:
        mostrar_menu_principal()
        opcion = input("Ingrese una opción: ").strip()

        if opcion == "1":
            archivo = input("Ingrese el nombre del archivo (ej: productos.txt): ").strip()
            datos = leer_datos(archivo)
            if datos:
                productos, capacidad = datos
                print(f"\nDatos cargados correctamente. Capacidad de mochila: {capacidad}")
                print(f"Productos cargados: {len(productos)}")
            else:
                print("Error al leer el archivo o archivo vacío.")

        elif opcion == "2":
            if not productos:
                print("Debe cargar primero un archivo de productos (opción 1).")
                continue

            tipo = seleccionar_tipo_metaheuristica()
            heuristicas_sel = seleccionar_heuristicas(tipo)

            print("\n=== RESUMEN DE CONFIGURACIÓN ===")
            print(f"Tipo: {tipo}")
            print(f"Heurísticas seleccionadas: {', '.join(heuristicas_sel)}")
            print(f"Capacidad de mochila: {capacidad}")

            for h in heuristicas_sel:
                ejecutar_heuristica(h, productos, capacidad)

        elif opcion == "3":
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
