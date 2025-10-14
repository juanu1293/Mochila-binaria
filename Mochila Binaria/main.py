# main.py

import importlib
from lector_archivo import leer_productos

# ===========================================================
# Diccionario actualizado de metaheurísticas y heurísticas
# ===========================================================

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

# ===========================================================
# Funciones de menú
# ===========================================================

def mostrar_menu_principal():
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Cargar datos de productos")
    print("2. Configurar metaheurística y heurísticas")
    print("3. Ejecutar heurísticas seleccionadas")
    print("4. Salir")


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
                print("⚠️ Opción inválida.")
        except ValueError:
            print("⚠️ Ingrese un número válido.")


def seleccionar_heuristicas(tipo):
    heuristicas = METAHEURISTICAS[tipo]
    print(f"\nHeurísticas disponibles para {tipo}:\n")
    for i, h in enumerate(heuristicas, start=1):
        print(f"{i}. {h}")

    if len(heuristicas) == 1:
        return heuristicas

    print("\nSeleccione varias separadas por coma (ej: 1,3,5)")
    seleccion = input("Seleccione heurísticas: ")

    seleccionadas = []
    try:
        indices = [int(x.strip()) for x in seleccion.split(',')]
        for i in indices:
            if 1 <= i <= len(heuristicas):
                seleccionadas.append(heuristicas[i - 1])
    except ValueError:
        print("⚠️ Entrada inválida.")
    return seleccionadas


# ===========================================================
# Ejecutar heurísticas
# ===========================================================

def ejecutar_heuristica(nombre, productos, capacidad, seleccionadas):
    """
    Carga dinámicamente el módulo correspondiente y ejecuta la función principal.
    """

    # Mapeo entre nombre descriptivo y archivo Python
    archivos = {
        "Mayor costo": "heuristica_mayor_costo",
        "Menor volumen": "heuristica_menor_volumen",
        "Mayor combinación lineal de factores": "heuristica_combinacion_lineal",
        "Menor combinación lineal de factores": "heuristica_combinacion_lineal",
        "Mayor costo/volumen": "heuristica_costo_volumen",
        "Menor costo/volumen": "heuristica_costo_volumen",
        "Azar": "heuristica_azar",
        "Alternancia": "heuristica_alternancia",
        "Menor capacidad residual libre": "heuristica_capacidad_residual",
        "Menor costo": "heuristica_menor_costo",
        "Mayor volumen": "heuristica_mayor_volumen",
        "Dividir en submochilas": "heuristica_dividir_submochilas"
    }

    modulo_nombre = archivos.get(nombre)
    if not modulo_nombre:
        print(f"⚠️ No hay implementación para {nombre}")
        return

    try:
        modulo = importlib.import_module(f"heuristicas.{modulo_nombre}")
    except ModuleNotFoundError:
        print(f"⚠️ No se encontró el módulo para {nombre}")
        return

    # ---------------------
    # Configuración especial
    # ---------------------
    parametros = {}

    if "combinación lineal" in nombre.lower():
        repeticiones = int(input("¿Cuántas veces desea ejecutar la heurística?: "))
        parametros["repeticiones"] = repeticiones
        parametros["factores"] = []
        for i in range(repeticiones):
            k1 = float(input(f"Ingrese k1 para ejecución {i+1}: "))
            k2 = float(input(f"Ingrese k2 para ejecución {i+1}: "))
            parametros["factores"].append((k1, k2))

    elif nombre.lower() == "azar":
        raiz = int(input("Ingrese la semilla (raíz) para la aleatoriedad: "))
        parametros["raiz"] = raiz

    elif nombre.lower() == "alternancia":
        print("\nDebe elegir 2 o 3 heurísticas ya seleccionadas para alternar.")
        for i, h in enumerate(seleccionadas, start=1):
            print(f"{i}. {h}")
        seleccion = input("Seleccione heurísticas para alternar (ej: 1,3): ")
        indices = [int(x.strip()) for x in seleccion.split(',')]
        heur_alternar = [seleccionadas[i-1] for i in indices if 1 <= i <= len(seleccionadas)]
        parametros["alternar"] = heur_alternar

    # Ejecutar función principal de la heurística
    print(f"\n▶ Ejecutando heurística: {nombre}")
    modulo.ejecutar(productos, capacidad, parametros)


# ===========================================================
# Programa principal
# ===========================================================

def main():
    productos = []
    mochila_capacidad = None
    tipo_seleccionado = None
    heuristicas_seleccionadas = []

    while True:
        mostrar_menu_principal()
        opcion = input("\nIngrese una opción: ").strip()

        if opcion == "1":
            archivo = input("Ingrese el nombre del archivo (ej: productos.txt): ").strip()
            productos = leer_productos(archivo)
            if productos:
                print(f"\n✅ {len(productos)} productos cargados correctamente.")
            else:
                print("\n⚠️ No se cargaron productos.")

        elif opcion == "2":
            if not productos:
                print("\n⚠️ Primero debe cargar un archivo de productos (opción 1).")
                continue

            try:
                mochila_capacidad = float(input("\nIngrese la capacidad de la mochila: "))
            except ValueError:
                print("⚠️ Capacidad inválida.")
                continue

            tipo_seleccionado = seleccionar_tipo_metaheuristica()
            heuristicas_seleccionadas = seleccionar_heuristicas(tipo_seleccionado)

            print("\n=== CONFIGURACIÓN GUARDADA ===")
            print(f"Capacidad: {mochila_capacidad}")
            print(f"Tipo: {tipo_seleccionado}")
            print(f"Heurísticas: {', '.join(heuristicas_seleccionadas)}")

        elif opcion == "3":
            if not heuristicas_seleccionadas:
                print("\n⚠️ No hay heurísticas seleccionadas (use opción 2).")
                continue

            usados = set()  # Para evitar repetir productos
            for heuristica in heuristicas_seleccionadas:
                ejecutar_heuristica(heuristica, productos, mochila_capacidad, heuristicas_seleccionadas)
                usados.update([p['nombre'] for p in productos])  # Control futuro

        elif opcion == "4":
            print("\nSaliendo del programa... 👋")
            break

        else:
            print("⚠️ Opción no válida.")


if __name__ == "__main__":
    main()
