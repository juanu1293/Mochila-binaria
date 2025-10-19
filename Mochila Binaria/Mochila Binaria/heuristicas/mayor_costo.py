# heuristicas/mayor_costo.py

import os

def heuristica_mayor_costo(productos, capacidad):
    productos_ordenados = sorted(productos, key=lambda x: x['costo'], reverse=True)

    seleccionados = []
    volumen_actual = 0
    costo_total = 0

    for producto in productos_ordenados:
        if volumen_actual + producto['volumen'] <= capacidad:
            seleccionados.append(producto)
            volumen_actual += producto['volumen']
            costo_total += producto['costo']
        else:
            break

    vector_solucion = []
    nombres_seleccionados = {p['nombre'] for p in seleccionados}
    for p in productos:
        vector_solucion.append(1 if p['nombre'] in nombres_seleccionados else 0)

    print("\n=== RESULTADOS: Heurística de Mayor Costo ===")
    print(f"{'Producto':<15} {'Costo':<10} {'Volumen':<10}")
    print("-" * 40)
    for p in seleccionados:
        print(f"{p['nombre']:<15} {p['costo']:<10} {p['volumen']:<10}")
    print("-" * 40)
    print(f"Volumen total ocupado: {volumen_actual}")
    print(f"Costo total: {costo_total}")
    print(f"Vector solución: {vector_solucion}")

    guardar_resultados(seleccionados, volumen_actual, costo_total, vector_solucion, capacidad)

    return {
        'seleccionados': seleccionados,
        'volumen_total': volumen_actual,
        'costo_total': costo_total,
        'vector': vector_solucion
    }


def guardar_resultados(seleccionados, volumen_total, costo_total, vector, capacidad):
    os.makedirs("resultados", exist_ok=True)
    ruta = os.path.join("resultados", "resultado_mochila.txt")

    # Escribir en modo append
    with open(ruta, "a", encoding="utf-8") as f:
        f.write("=== RESULTADOS: Heurística de Mayor Costo ===\n")
        f.write(f"Capacidad de mochila: {capacidad}\n\n")
        f.write(f"{'Producto':<15} {'Costo':<10} {'Volumen':<10}\n")
        f.write("-" * 40 + "\n")
        for p in seleccionados:
            f.write(f"{p['nombre']:<15} {p['costo']:<10} {p['volumen']:<10}\n")
        f.write("-" * 40 + "\n")
        f.write(f"Volumen total ocupado: {volumen_total}\n")
        f.write(f"Costo total: {costo_total}\n")
        f.write(f"Vector solución: {vector}\n\n")

    print(f"Resultados guardados en: {ruta}")
