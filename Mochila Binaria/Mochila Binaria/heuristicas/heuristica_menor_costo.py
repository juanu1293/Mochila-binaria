# heuristicas/heuristica_menor_costo.py

def ejecutar(productos, capacidad, parametros):
    usados = set()
    seleccion = []
    for p in sorted(productos, key=lambda x: x['costo']):
        if p['nombre'] not in usados and p['volumen'] <= capacidad:
            seleccion.append(p)
            usados.add(p['nombre'])
            capacidad -= p['volumen']

    print("=== Menor Costo ===")
    for p in seleccion:
        print(f"{p['nombre']} - Costo: {p['costo']} - Volumen: {p['volumen']}")

    # Guardar en archivo de resultados
    with open("resultados_reduccion.txt", "a") as f:
        f.write("=== Menor Costo ===\n")
        for p in seleccion:
            f.write(f"{p['nombre']} - Costo: {p['costo']} - Volumen: {p['volumen']}\n")
        f.write("\n")
