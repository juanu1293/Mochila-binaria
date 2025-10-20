# heuristicas/heuristica_menor_combinacion_lineal.py

def ejecutar(productos, capacidad, parametros):
    repeticiones = parametros.get("repeticiones", 1)
    factores = parametros.get("factores", [(1,1)]*repeticiones)
    usados = set()

    for i in range(repeticiones):
        k1, k2 = factores[i]
        seleccion = []
        for p in sorted(productos, key=lambda x: k1*x['costo'] + k2*x['volumen']):
            if p['nombre'] not in usados and p['volumen'] <= capacidad:
                seleccion.append(p)
                usados.add(p['nombre'])
                capacidad -= p['volumen']
        print(f"=== Menor Combinación Lineal Ejecución {i+1} (k1={k1}, k2={k2}) ===")
        for p in seleccion:
            print(f"{p['nombre']} - Costo: {p['costo']} - Volumen: {p['volumen']}")

        with open("resultados_reduccion.txt", "a") as f:
            f.write(f"=== Menor Combinación Lineal Ejecución {i+1} (k1={k1}, k2={k2}) ===\n")
            for p in seleccion:
                f.write(f"{p['nombre']} - Costo: {p['costo']} - Volumen: {p['volumen']}\n")
            f.write("\n")
