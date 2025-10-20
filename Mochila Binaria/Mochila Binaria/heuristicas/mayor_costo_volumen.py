import os

def heuristica_mayor_costo_volumen(productos, capacidad):
    """
    Heurística constructiva: Mayor costo/volumen.
    Selecciona productos con el mayor ratio costo/volumen hasta llenar o casi llenar la mochila,
    sin sobrepasar la capacidad y deteniéndose cuando el siguiente producto no cabe.
    """

    # Calcular ratio costo/volumen
    productos_ratio = []
    for p in productos:
        if p['volumen'] > 0:
            ratio = p['costo'] / p['volumen']
        else:
            ratio = 0
        productos_ratio.append({
            'nombre': p['nombre'],
            'costo': p['costo'],
            'volumen': p['volumen'],
            'ratio': ratio
        })

    # Ordenar por ratio descendente (mayor primero)
    productos_ordenados = sorted(productos_ratio, key=lambda x: x['ratio'], reverse=True)

    seleccionados = []
    volumen_actual = 0
    costo_total = 0

    for producto in productos_ordenados:
        if volumen_actual + producto['volumen'] <= capacidad:
            seleccionados.append(producto)
            volumen_actual += producto['volumen']
            costo_total += producto['costo']
        else:
            break  # el siguiente producto no cabe

    # Crear vector solución
    vector_solucion = []
    nombres_sel = {p['nombre'] for p in seleccionados}
    for p in productos:
        vector_solucion.append(1 if p['nombre'] in nombres_sel else 0)

    # Mostrar resultados por consola
    print("\n=== RESULTADOS: Heurística de Mayor Costo/Volumen ===")
    print(f"{'Producto':<15} {'Costo':<10} {'Volumen':<10} {'C/V':<10}")
    print("-" * 50)
    for p in seleccionados:
        ratio = round(p['costo'] / p['volumen'], 3) if p['volumen'] > 0 else 0
        print(f"{p['nombre']:<15} {p['costo']:<10} {p['volumen']:<10} {ratio:<10}")
    print("-" * 50)
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
        f.write("\n=== RESULTADOS: Heurística de Mayor Costo/Volumen ===\n")
        f.write(f"Capacidad de mochila: {capacidad}\n\n")
        f.write(f"{'Producto':<15} {'Costo':<10} {'Volumen':<10} {'C/V':<10}\n")
        f.write("-" * 50 + "\n")
        for p in seleccionados:
            ratio = round(p['costo'] / p['volumen'], 3) if p['volumen'] > 0 else 0
            f.write(f"{p['nombre']:<15} {p['costo']:<10} {p['volumen']:<10} {ratio:<10}\n")
        f.write("-" * 50 + "\n")
        f.write(f"Volumen total ocupado: {volumen_total}\n")
        f.write(f"Costo total: {costo_total}\n")
        f.write(f"Vector solución: {vector}\n")
        f.write("=" * 50 + "\n")

    print("Resultados guardados correctamente en archivo.")
