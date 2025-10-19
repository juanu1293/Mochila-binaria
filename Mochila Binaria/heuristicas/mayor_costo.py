# heuristicas/mayor_costo.py

def heuristica_mayor_costo(productos, capacidad):
    """
    Heurística constructiva: Mayor costo.
    Selecciona productos con los mayores costos hasta llenar (o casi llenar) la mochila,
    sin sobrepasar la capacidad y deteniéndose cuando el siguiente producto no cabe.
    
    productos: lista de diccionarios con claves {'nombre', 'costo', 'volumen'}
    capacidad: capacidad total de la mochila
    """

    # Ordenar los productos por costo (descendente)
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
            # Si el siguiente producto no cabe, termina el proceso
            break

    # Crear el vector solución
    vector_solucion = []
    nombres_seleccionados = {p['nombre'] for p in seleccionados}
    for p in productos:
        if p['nombre'] in nombres_seleccionados:
            vector_solucion.append(1)
        else:
            vector_solucion.append(0)

    # Mostrar resultados
    print("\n=== RESULTADOS: Heurística de Mayor Costo ===")
    print(f"{'Producto':<15} {'Costo':<10} {'Volumen':<10}")
    print("-" * 40)
    for p in seleccionados:
        print(f"{p['nombre']:<15} {p['costo']:<10} {p['volumen']:<10}")

    print("-" * 40)
    print(f"Volumen total ocupado: {volumen_actual}")
    print(f"Costo total: {costo_total}")
    print(f"Vector solución: {vector_solucion}")

    # Retornar resultados por si se quieren usar después
    return {
        'seleccionados': seleccionados,
        'volumen_total': volumen_actual,
        'costo_total': costo_total,
        'vector': vector_solucion
    }
