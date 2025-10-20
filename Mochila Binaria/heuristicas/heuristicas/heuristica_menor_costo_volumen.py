# heuristicas/heuristica_menor_costo_volumen.py

def ejecutar(productos, capacidad, parametros):
    usados = set()
    seleccion = []
    for p in sorted(productos, key=lambda x: x['costo']/x['volumen']):
        if p['nombre'] not in usados and p['volumen'] <= capacidad:
            seleccion.append(p)
            usados.add(p['nombre'])
            capacidad -= p['volumen']

    print("=== Menor Costo/Volumen ===")
    for p in seleccion:
        print(f"{p['nombre']} - Costo: {p['costo']} - Volumen: {p['volumen']}")

    with open("resultados_reduccion.txt", "a") as f:
        f.write("=== Menor Costo/Volumen ===\n")
        for p in seleccion:
            f.write(f"{p['nombre']} - Costo: {p['costo']} - Volumen: {p['volumen']}\n")
        f.write("\n")
