import os
import random

def heuristica_azar(productos, capacidad):
    """
    Heurística constructiva: Selección aleatoria de productos.
    - Solicita una semilla para el generador aleatorio.
    - Selecciona productos aleatoriamente sin repetir.
    - No supera la capacidad de la mochila.
    """

    # Solicitar semilla al usuario
    try:
        semilla = int(input("\nIngrese la semilla para la heurística de azar: "))
    except ValueError:
        print("Semilla inválida, se usará el valor por defecto (0).")
        semilla = 0

    random.seed(semilla)

    # Mezclar productos aleatoriamente
    productos_azar = productos.copy()
    random.shuffle(productos_azar)

    seleccionados = []
    volumen_actual = 0
    costo_total = 0

    for producto in productos_azar:
        if volumen_actual + producto['volumen'] <= capacidad:
            seleccionados.append(producto)
            volumen_actual += producto['volumen']
            costo_total += producto['costo']
        else:
            # Si el siguiente producto ya no cabe, se detiene
            break

    # Crear vector solución (1 = seleccionado, 0 = no seleccionado)
    nombres_sel = {p['nombre'] for p in seleccionados}
    vector_solucion = [1 if p['nombre'] in nombres_sel else 0 for p in productos]

    # Mostrar resultados por consola
    print("\n=== RESULTADOS: Heurística de Azar ===")
    print(f"Semilla usada: {semilla}")
    print(f"{'Producto':<15} {'Costo':<10} {'Volumen':<10}")
    print("-" * 40)
    for p in seleccionados:
        print(f"{p['nombre']:<15} {p['costo']:<10} {p['volumen']:<10}")
    print("-" * 40)
    print(f"Volumen total ocupado: {volumen_actual}")
    print(f"Costo total: {costo_total}")
    print(f"Vector solución: {vector_solucion}")

    # Guardar resultados
    guardar_resultados(seleccionados, volumen_actual, costo_total, vector_solucion, capacidad, semilla)

    return {
        'seleccionados': seleccionados,
        'volumen_total': volumen_actual,
        'costo_total': costo_total,
        'vector': vector_solucion,
        'semilla': semilla
    }


def guardar_resultados(seleccionados, volumen_total, costo_total, vector, capacidad, semilla):
    """Guarda los resultados de la heurística de azar en el archivo general."""
    os.makedirs("resultados", exist_ok=True)
    ruta = os.path.join("resultados", "resultado_mochila.txt")

    with open(ruta, "a", encoding="utf-8") as f:
        f.write("\n=== RESULTADOS: Heurística de Azar ===\n")
        f.write(f"Capacidad de mochila: {capacidad}\n")
        f.write(f"Semilla usada: {semilla}\n\n")
        f.write(f"{'Producto':<15} {'Costo':<10} {'Volumen':<10}\n")
        f.write("-" * 40 + "\n")
        for p in seleccionados:
            f.write(f"{p['nombre']:<15} {p['costo']:<10} {p['volumen']:<10}\n")
        f.write("-" * 40 + "\n")
        f.write(f"Volumen total ocupado: {volumen_total}\n")
        f.write(f"Costo total: {costo_total}\n")
        f.write(f"Vector solución: {vector}\n")
        f.write("=" * 50 + "\n")

    print("Resultados guardados correctamente en archivo.")
