def heuristica_mayor_combinacion_lineal(productos, capacidad):
    """
    Heurística: Mayor combinación lineal (k1*costo + k2*volumen).
    - Se repite entre 1 y 11 veces.
    - k1 se ingresa manualmente (0.0 a 1.0), k2 = 1 - k1.
    - Se muestra cada resultado en consola.
    - Se guarda todo en 'resultados.txt'.
    - Se devuelve solo la mejor iteración (mayor costo_total).
    """

    resultados_iter = []

    # Pedir número de repeticiones
    while True:
        try:
            repeticiones = int(input("¿Cuántas veces desea ejecutar la heurística (1-11)? "))
            if 1 <= repeticiones <= 11:
                break
            print("Debe estar entre 1 y 11.")
        except ValueError:
            print("Ingrese un número entero válido.")

    for i in range(repeticiones):
        print(f"\n=== Iteración {i+1} ===")

        # pedir k1
        while True:
            try:
                k1 = float(input(f"Ingrese k1 para la iteración {i+1} (0.0 - 1.0): "))
                if 0.0 <= k1 <= 1.0:
                    break
                print("k1 debe estar entre 0.0 y 1.0.")
            except ValueError:
                print("Ingrese un número válido (float).")
        k2 = 1.0 - k1

        # calcular valor combinado
        productos_val = []
        for p in productos:
            valor = k1 * p['costo'] + k2 * p['volumen']
            productos_val.append({
                'nombre': p['nombre'],
                'costo': p['costo'],
                'volumen': p['volumen'],
                'valor_combinado': valor
            })

        # ordenar descendente
        productos_ordenados = sorted(productos_val, key=lambda x: x['valor_combinado'], reverse=True)

        # selección tipo "mayor costo"
        seleccionados = []
        volumen_total = 0.0
        costo_total = 0.0
        for p in productos_ordenados:
            if volumen_total + p['volumen'] <= capacidad:
                seleccionados.append(p)
                volumen_total += p['volumen']
                costo_total += p['costo']

        # generar vector solución
        nombres_sel = {s['nombre'] for s in seleccionados}
        vector_solucion = [1 if p['nombre'] in nombres_sel else 0 for p in productos]

        # Mostrar resultado en consola
        print(f"=== RESULTADOS: Heurística Mayor Combinación Lineal (Iteración {i+1}) ===")
        print(f"k1 = {k1:.2f}, k2 = {k2:.2f}")
        print(f"{'Producto':<15}{'Costo':<10}{'Volumen':<10}{'ValorComb':<12}")
        print("-" * 50)
        for s in seleccionados:
            print(f"{s['nombre']:<15}{s['costo']:<10}{s['volumen']:<10}{s['valor_combinado']:<12.2f}")
        print("-" * 50)
        print(f"Volumen total ocupado: {volumen_total}")
        print(f"Costo total: {costo_total}")
        print(f"Vector solución: {vector_solucion}\n")

        # guardar resultado de esta iteración
        with open("resultados.txt", "a", encoding="utf-8") as f:
            f.write("=== RESULTADOS: Heurística Mayor Combinación Lineal ===\n")
            f.write(f"Iteración {i+1} - k1={k1:.2f}, k2={k2:.2f}\n")
            f.write(f"{'Producto':<15}{'Costo':<10}{'Volumen':<10}{'ValorComb':<12}\n")
            f.write("-" * 50 + "\n")
            for s in seleccionados:
                f.write(f"{s['nombre']:<15}{s['costo']:<10}{s['volumen']:<10}{s['valor_combinado']:<12.2f}\n")
            f.write("-" * 50 + "\n")
            f.write(f"Volumen total ocupado: {volumen_total}\n")
            f.write(f"Costo total: {costo_total}\n")
            f.write(f"Vector solución: {vector_solucion}\n\n")

        resultados_iter.append({
            'k1': k1,
            'k2': k2,
            'seleccionados': seleccionados,
            'volumen_total': volumen_total,
            'costo_total': costo_total,
            'vector': vector_solucion
        })

    # seleccionar la mejor (según mayor costo_total)
    if not resultados_iter:
        return None

    mejor = max(resultados_iter, key=lambda x: x['costo_total'])

    # guardar la mejor en el archivo
    with open("resultados.txt", "a", encoding="utf-8") as f:
        f.write("=== MEJOR ITERACIÓN (Mayor combinación lineal) ===\n")
        f.write(f"k1={mejor['k1']:.2f}, k2={mejor['k2']:.2f}\n")
        f.write(f"Volumen total ocupado: {mejor['volumen_total']}\n")
        f.write(f"Costo total: {mejor['costo_total']}\n")
        f.write(f"Vector solución: {mejor['vector']}\n\n")

    # retornar al main la mejor
    return {
        'seleccionados': mejor['seleccionados'],
        'volumen_total': mejor['volumen_total'],
        'costo_total': mejor['costo_total'],
        'vector': mejor['vector']
    }
