import os
from lector_archivo import leer_datos
from heuristicas.mayor_costo import heuristica_mayor_costo
from heuristicas.menor_volumen import heuristica_menor_volumen
from heuristicas.mayor_costo_volumen import heuristica_mayor_costo_volumen
from heuristicas.azar_const import heuristica_azar




def limpiar_archivo_resultados():
    """Elimina el contenido del archivo de resultados antes de ejecutar heurísticas nuevas."""
    os.makedirs("resultados", exist_ok=True)
    ruta = os.path.join("resultados", "resultado_mochila.txt")
    open(ruta, "w").close()
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
        "Constructivas": ["Mayor costo", "Menor volumen", "Mayor costo/volumen", "Mayor Combinacion Lineal",
                          "Azar Const", "Alternancia Const", "Menor Capacidad Residual"],
        "De reducción": ["Menor costo", "Mayor volumen", "Menor Combinacion lineal", "Menos costo/volumen",
                         "Azar Redu", "Alternancia Redu"],
        "De descomposición": ["Dividir en sub mochilas"]
    }

    print(f"\n=== HEURÍSTICAS DISPONIBLES ({tipo}) ===")
    lista = heuristicas_disponibles[tipo]

    for i, h in enumerate(lista, start=1):
        print(f"{i}. {h}")

    print("\nPuede seleccionar varias heurísticas separadas por comas (ej: 1,2):")
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
    """Ejecuta la heurística seleccionada y devuelve el resultado."""
    print(f"\nEjecutando heurística: {nombre_heuristica}")

    if nombre_heuristica.lower() == "mayor costo":
        return heuristica_mayor_costo(productos, capacidad)
    elif nombre_heuristica.lower() == "menor volumen":
        return heuristica_menor_volumen(productos, capacidad)
    elif nombre_heuristica.lower() == "mayor costo/volumen":
        return heuristica_mayor_costo_volumen(productos, capacidad)
    elif nombre_heuristica.lower() == "azar const":
        return heuristica_azar(productos, capacidad)
    else:
        print(f"La heurística '{nombre_heuristica}' aún no está implementada.")
        return None


def guardar_mejor_resultado(mejor):
    """Guarda el resumen del mejor resultado al final del archivo."""
    ruta = os.path.join("resultados", "resultado_mochila.txt")
    with open(ruta, "a", encoding="utf-8") as f:
        f.write("\n=== MEJOR RESULTADO GLOBAL ===\n")
        f.write(f"Heurística ganadora: {mejor['nombre']}\n")
        f.write(f"Volumen total: {mejor['volumen_total']}\n")
        f.write(f"Costo total: {mejor['costo_total']}\n")
        f.write(f"Vector solución: {mejor['vector']}\n")
        f.write("=" * 40 + "\n")

    print("\n=== MEJOR RESULTADO GLOBAL ===")
    print(f"Heurística ganadora: {mejor['nombre']}")
    print(f"Volumen total: {mejor['volumen_total']}")
    print(f"Costo total: {mejor['costo_total']}")
    print(f"Vector solución: {mejor['vector']}")


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

            # Vaciar archivo antes de iniciar ejecución
            limpiar_archivo_resultados()

            print("\n=== RESUMEN DE CONFIGURACIÓN ===")
            print(f"Tipo: {tipo}")
            print(f"Heurísticas seleccionadas: {', '.join(heuristicas_sel)}")
            print(f"Capacidad de mochila: {capacidad}")

            resultados = []
            for h in heuristicas_sel:
                resultado = ejecutar_heuristica(h, productos, capacidad)
                if resultado:
                    resultado["nombre"] = h
                    resultados.append(resultado)

            # Comparar resultados
            if resultados:
                mejor = max(resultados, key=lambda x: x["costo_total"])
                guardar_mejor_resultado(mejor)
            else:
                print("No se ejecutaron heurísticas válidas.")

        elif opcion == "3":
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
