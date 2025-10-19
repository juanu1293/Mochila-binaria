import os
from lector_archivo import leer_datos
from heuristicas.mayor_costo import heuristica_mayor_costo


def limpiar_archivo_resultados():
    """Elimina el contenido del archivo de resultados antes de ejecutar heurísticas nuevas."""
    os.makedirs("resultados", exist_ok=True)
    ruta = os.path.join("resultados", "resultado_mochila.txt")
    open(ruta, "w").close()  # Vacía el archivo
    print("\nArchivo de resultados vaciado correctamente.")


def seleccionar_tipo_metaheuristica():
    """Permite al usuario elegir el tipo de metaheurística."""
    print("\n=== SELECCIONAR TIPO DE METAHEURÍSTICA ===")
    print("1. Constructivas")
    print("2. De reducción")
    print("3. De descomposición")

    while True:
        opcion = input("Seleccione el tipo de metaheurística: ").strip()
        if opcion == "1":
            return "Constructivas"
        elif opcion == "2":
            return "De reducción"
        elif opcion == "3":
            return "De descomposición"
        else:
            print("Opción inválida. Intente nuevamente.")


def seleccionar_heuristicas(tipo):
    """Lista heurísticas disponibles según el tipo elegido y permite seleccionar varias."""
    heuristicas_disponibles = {
        "Constructivas": ["Mayor costo", "Menor volumen", "Mejor relación costo/volumen"],
        "De reducción": ["Eliminación por bajo costo", "Eliminación por alto volumen"],
        "De descomposición": ["División por categorías", "Agrupamiento por volumen"]
    }

    print(f"\n=== HEURÍSTICAS DISPONIBLES ({tipo}) ===")
    lista = heuristicas_disponibles[tipo]

    for i, h in enumerate(lista, start=1):
        print(f"{i}. {h}")

    print("\nPuede seleccionar varias heurísticas separadas por comas (ej: 1,3):")
    seleccion = input("Ingrese su selección: ").strip()
    indices = [s.strip() for s in seleccion.split(",") if s.strip().isdigit()]

    heuristicas_sel = []
    for i in indices:
        idx = int(i)
        if 1 <= idx <= len(lista):
            heuristicas_sel.append(lista[idx - 1])

    if not heuristicas_sel:
        print("No se seleccionó ninguna heurística válida. Se ejecutará la primera por defecto.")
        heuristicas_sel = [lista[0]]

    return heuristicas_sel


def ejecutar_heuristica(nombre_heuristica, productos, capacidad):
    """Ejecuta la heurística seleccionada."""
    print(f"\nEjecutando heurística: {nombre_heuristica}")
    if nombre_heuristica.lower() == "mayor costo":
        heuristica_mayor_costo(productos, capacidad)
    else:
        print(f"La heurística '{nombre_heuristica}' aún no está implementada.")


def main():
    productos = []
    capacidad = None

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Cargar datos de productos")
        print("2. Configurar y ejecutar metaheurística")
        print("3. Salir")

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

            # Vaciar el archivo antes de comenzar la ejecución
            limpiar_archivo_resultados()

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
