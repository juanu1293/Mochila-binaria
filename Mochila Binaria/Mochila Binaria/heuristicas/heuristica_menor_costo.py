def ejecutar_costo(productos, capacidad):
    """
    Heurística de reducción: Menor Costo.
    Comienza con todos los productos y elimina los de menor costo
    hasta que el volumen total esté dentro de la capacidad.
    """

    # Copiar productos originales
    seleccionados = productos[:]
    eliminados = []

    # Calcular volumen y costo total inicial
    volumen_total = sum(p['volumen'] for p in seleccionados)
    costo_total = sum(p['costo'] for p in seleccionados)

    # Mientras el volumen total supere la capacidad, eliminar el de menor costo
    while volumen_total > capacidad and seleccionados:
        # Buscar producto con menor costo
        producto_min = min(seleccionados, key=lambda x: x['costo'])
        seleccionados.remove(producto_min)
        eliminados.append(producto_min['nombre'])
        volumen_total -= producto_min['volumen']
        costo_total -= producto_min['costo']

    # Crear vector solución (1 si quedó seleccionado, 0 si fue eliminado)
    nombres_sel = {p['nombre'] for p in seleccionados}
    vector_solucion = [1 if p['nombre'] in nombres_sel else 0 for p in productos]

    # === Mostrar resultados ===
    print("\n=== RESULTADOS: Heurística Menor Costo ===")
    if eliminados:
        print("Orden de eliminación:")
        for i, nombre in enumerate(eliminados, 1):
            print(f"{i}. {nombre}")
    else:
        print("No se eliminaron productos (ya estaba dentro de la capacidad).")

    print("\nProductos finales seleccionados:")
    print(f"{'Producto':<15}{'Costo':<10}{'Volumen':<10}")
    print("-" * 40)
    for p in seleccionados:
        print(f"{p['nombre']:<15}{p['costo']:<10}{p['volumen']:<10}")
    print("-" * 40)
    print(f"Volumen total ocupado: {volumen_total}")
    print(f"Costo total: {costo_total}")
    print(f"Vector solución: {vector_solucion}")

    # === Guardar resultados en archivo ===
    with open("resultados.txt", "a", encoding="utf-8") as f:
        f.write("=== RESULTADOS: Heurística Menor Costo ===\n")
        if eliminados:
            f.write("Orden de eliminación:\n")
            for i, nombre in enumerate(eliminados, 1):
                f.write(f"{i}. {nombre}\n")
        else:
            f.write("No se eliminaron productos (ya estaba dentro de la capacidad).\n")

        f.write("\nProductos finales seleccionados:\n")
        f.write(f"{'Producto':<15}{'Costo':<10}{'Volumen':<10}\n")
        f.write("-" * 40 + "\n")
        for p in seleccionados:
            f.write(f"{p['nombre']:<15}{p['costo']:<10}{p['volumen']:<10}\n")
        f.write("-" * 40 + "\n")
        f.write(f"Volumen total ocupado: {volumen_total}\n")
        f.write(f"Costo total: {costo_total}\n")
        f.write(f"Vector solución: {vector_solucion}\n\n")

    # === Retornar resultado estándar ===
    return {
        'seleccionados': seleccionados,
        'volumen_total': volumen_total,
        'costo_total': costo_total,
        'vector': vector_solucion
    }
