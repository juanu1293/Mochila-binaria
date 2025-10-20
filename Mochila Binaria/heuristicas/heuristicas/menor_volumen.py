import os

def heuristica_menor_volumen(productos, capacidad):
    """
    Heurística constructiva: Menor volumen.
    Selecciona productos con los menores volúmenes hasta llenar o casi llenar la mochila,
    sin sobrepasar la capacidad. Detiene el proceso si el siguiente producto no cabe.
    """

    # Ordenar los productos por volumen (ascendente)
    productos_ordenados = sorted(productos, key=lambda x: x['volumen'])

    seleccionados = []
    volumen_actual = 0
    costo_total = 0

    for producto in productos_ordenados:
        if volumen_actual + producto['volumen'] <= capacidad:
            seleccionados.append(producto)
            volumen_actual += producto['volumen']
            costo_total += producto['costo']
        else:
            break  # el siguiente no cabe, se termina

    # Crear el vector solución
    vector_solucion = []
    nombres_seleccionados = {p['nombre'] for p in seleccionados}
    for p in productos:
        vector_solucion.append(1 if p['nombre'] in nombres_seleccionados else 0)

    # Mostrar resultados por consola
    print("\n=== RESULTADOS: Heurística de Menor Volumen ===")
    print(f"{'Producto':<15} {'Costo':<10} {'Volumen':<10}")
    print("-" * 40)
    for p in seleccionados:
        print(f"{p['nombre']:<15} {p['costo']:<10} {p['volumen']:<10}")
    print("-" * 40)
    print(f"Volumen total ocupado: {volumen_actual}")
    print(f"Costo total: {costo_total}")
    print(f"Vector solución: {vector_solucion}")

    # Guardar resultados en archivo
    guardar_resultados(seleccionados, volumen_actual, costo_total, vector_solucion, capacidad)

    return {
        'seleccionados': seleccionados,
        'volumen_total': volumen_actual,
        'costo_total': costo_total,
        'vector': vector_solucion
    }


def guardar_resultados(seleccionados, volumen_total, costo_total, vector, capacidad):
    """Guarda los resultados de esta heurística en el archivo general de resultados."""
    os.makedirs("resultados", exist_ok=True)
    ruta = os.path.join("resultados", "resultado_mochila.txt")

    with open(ruta, "a", encoding="utf-8") as f:
        f.write("\n=== RESULTADOS: Heurística de Menor Volumen ===\n")
        f.write(f"Capacidad de mochila: {capacidad}\n\n")
        f.write(f"{'Producto':<15} {'Costo':<10} {'Volumen':<10}\n")
        f.write("-" * 40 + "\n")
        for p in seleccionados:
            f.write(f"{p['nombre']:<15} {p['costo']:<10} {p['volumen']:<10}\n")
        f.write("-" * 40 + "\n")
        f.write(f"Volumen total ocupado: {volumen_total}\n")
        f.write(f"Costo total: {costo_total}\n")
        f.write(f"Vector solución: {vector}\n")
        f.write("=" * 40 + "\n")

    print("Resultados guardados correctamente en archivo.")
