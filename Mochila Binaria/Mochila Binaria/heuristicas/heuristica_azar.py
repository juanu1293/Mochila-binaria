# heuristicas/heuristica_azar.py

import random

def ejecutar(productos, capacidad, parametros):
    raiz = parametros.get("raiz", None)
    if raiz is not None:
        random.seed(raiz)

    copia = productos.copy()
    random.shuffle(copia)
    usados = set()
    seleccion = []

    for p in copia:
        if p['nombre'] not in usados and p['volumen'] <= capacidad:
            seleccion.append(p)
            usados.add(p['nombre'])
            capacidad -= p['volumen']

    print("=== Azar ===")
    for p in seleccion:
        print(f"{p['nombre']} - Costo: {p['costo']} - Volumen: {p['volumen']}")

    with open("resultados_reduccion.txt", "a") as f:
        f.write("=== Azar ===\n")
        for p in seleccion:
            f.write(f"{p['nombre']} - Costo: {p['costo']} - Volumen: {p['volumen']}\n")
        f.write("\n")
