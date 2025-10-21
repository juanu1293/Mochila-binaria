# ...existing code...
def heuristica_menor_cap_residual_libre(productos, capacidad):
    # Ordenar productos de mayor a menor volumen
    productos_ordenados = sorted(productos, key=lambda x: x['volumen'], reverse=True)

    seleccionados = []
    volumen_total = 0
    costo_total = 0

    for prod in productos_ordenados:
        if volumen_total + prod['volumen'] <= capacidad:
            # Si cabe, agregar
            seleccionados.append(prod)
            volumen_total += prod['volumen']
            costo_total += prod['costo']
        else:
            # Intentar reemplazar el último por este para mejorar el llenado
            if seleccionados:
                for i in range(len(seleccionados)):
                    temp_vol = volumen_total - seleccionados[i]['volumen'] + prod['volumen']
                    if temp_vol <= capacidad and temp_vol > volumen_total:
                        # Hacer el reemplazo
                        volumen_total = temp_vol
                        costo_total = costo_total - seleccionados[i]['costo'] + prod['costo']
                        seleccionados[i] = prod
                        break

    # --- PASADA ADICIONAL: intentar añadir items no seleccionados que quepan en la capacidad restante ---
    restantes = [p for p in productos if p not in seleccionados]
    # Ordenar por volumen ascendente para intentar llenar huecos pequeños (favorece Producto2 en tu caso)
    restantes_ordenados = sorted(restantes, key=lambda x: x['volumen'])
    for prod in restantes_ordenados:
        if volumen_total + prod['volumen'] <= capacidad:
            seleccionados.append(prod)
            volumen_total += prod['volumen']
            costo_total += prod['costo']

    # Crear vector solución (mantiene el orden original de 'productos')
    vector_solucion = [1 if p in seleccionados else 0 for p in productos]

    # === SALIDA EN CONSOLA ===
    print("\n=== RESULTADOS: Heurística Menor Capacidad Residual Libre ===")
    print(f"{'Producto':<15}{'Costo':<10}{'Volumen':<10}")
    print("-" * 40)
    for p in seleccionados:
        print(f"{p['nombre']:<15}{p['costo']:<10}{p['volumen']:<10}")
    print("-" * 40)
    print(f"Volumen total ocupado: {volumen_total}")
    print(f"Costo total: {costo_total}")
    print(f"Vector solución: {vector_solucion}")

    # === GUARDAR EN ARCHIVO ===
    with open("resultados.txt", "a", encoding="utf-8") as f:
        f.write("=== RESULTADOS: Heurística Menor Capacidad Residual Libre ===\n")
        f.write(f"{'Producto':<15}{'Costo':<10}{'Volumen':<10}\n")
        f.write("-" * 40 + "\n")
        for p in seleccionados:
            f.write(f"{p['nombre']:<15}{p['costo']:<10}{p['volumen']:<10}\n")
        f.write("-" * 40 + "\n")
        f.write(f"Volumen total ocupado: {volumen_total}\n")
        f.write(f"Costo total: {costo_total}\n")
        f.write(f"Vector solución: {vector_solucion}\n\n")

    return {
        'seleccionados': seleccionados,
        'volumen_total': volumen_total,
        'costo_total': costo_total,
        'vector': vector_solucion
    }
