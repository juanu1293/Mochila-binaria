import os
import random

def heuristica_alternancia_constructiva(productos, capacidad):
    """
    Heurística alternancia - constructiva.
    Permite al usuario elegir hasta 3 heurísticas constructivas y alterna entre ellas
    para seleccionar ítems sin repetir hasta que no quepa nada más.

    Heurísticas base soportadas: 'Mayor costo', 'Menor volumen', 'Mayor costo/volumen', 'Azar'
    """
    print("\n=== Alternancia (Constructiva) ===")
    print("Puede elegir hasta 3 heurísticas a alternar en el orden deseado.")
    opciones = ['Mayor costo', 'Menor volumen', 'Mayor costo/volumen', 'Azar']
    for i, o in enumerate(opciones, 1):
        print(f"{i}. {o}")

    seleccion = input("Ingrese índices separados por coma (ej: 1,3): ").strip()
    indices = [s.strip() for s in seleccion.split(',') if s.strip().isdigit()]
    heur_sel = []
    for idx in indices[:3]:
        i = int(idx)
        if 1 <= i <= len(opciones):
            heur_sel.append(opciones[i - 1])

    if not heur_sel:
        print("No se seleccionó heurística válida. Usando 'Mayor costo' por defecto.")
        heur_sel = ['Mayor costo']

    # semillas para azar si se usa
    seed = None
    if 'Azar' in heur_sel:
        try:
            seed = int(input("Ingrese semilla para heurística 'Azar' (entero): "))
        except ValueError:
            seed = 0
        random.seed(seed)

    seleccionados = set()
    volumen_actual = 0
    costo_total = 0

    # precomputar listas ordenadas por heurística (listas de objetos)
    listas = {}
    listas['Mayor costo'] = sorted(productos, key=lambda x: x['costo'], reverse=True)
    listas['Menor volumen'] = sorted(productos, key=lambda x: x['volumen'])
    listas['Mayor costo/volumen'] = sorted(productos, key=lambda x: (x['costo'] / x['volumen'] if x['volumen'] > 0 else float('inf')), reverse=True)
    listas['Azar'] = productos.copy()

    # índices de posición para cada lista
    indices_pos = {k: 0 for k in listas}

    progreso = True
    while progreso:
        progreso = False
        for h in heur_sel:
            if h == 'Azar':
                random.shuffle(listas['Azar'])

            lista = listas[h]
            pos = indices_pos[h]
            elegido = None
            while pos < len(lista):
                p = lista[pos]
                pos += 1
                if p['nombre'] in seleccionados:
                    continue
                if volumen_actual + p['volumen'] <= capacidad:
                    elegido = p
                    break
            indices_pos[h] = pos

            if elegido:
                seleccionados.add(elegido['nombre'])
                volumen_actual += elegido['volumen']
                costo_total += elegido['costo']
                progreso = True

    # construir vector solución en orden original
    vector = [1 if p['nombre'] in seleccionados else 0 for p in productos]

    # mostrar y guardar
    print("\n=== RESULTADOS: Alternancia (Constructiva) ===")
    print(f"Heurísticas alternadas: {heur_sel}")
    print(f"Volumen total ocupado: {volumen_actual}")
    print(f"Costo total: {costo_total}")
    print(f"Vector solución: {vector}")

    guardar_resultados(seleccionados, volumen_actual, costo_total, vector, capacidad, 'Alternancia-Const', seed)

    seleccionados_list = [p for p in productos if p['nombre'] in seleccionados]
    return {
        'seleccionados': seleccionados_list,
        'volumen_total': volumen_actual,
        'costo_total': costo_total,
        'vector': vector,
        'semilla': seed
    }


def guardar_resultados(seleccionados, volumen_total, costo_total, vector, capacidad, nombre, semilla=None):
    os.makedirs("resultados", exist_ok=True)
    ruta = os.path.join("resultados", "resultado_mochila.txt")
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(f"\n=== RESULTADOS: {nombre} ===\n")
        f.write(f"Capacidad de mochila: {capacidad}\n")
        if semilla is not None:
            f.write(f"Semilla: {semilla}\n")
        f.write(f"{'Producto':<15} {'Costo':<10} {'Volumen':<10}\n")
        f.write("-" * 40 + "\n")
        # si recibimos un set de nombres, escribir solo nombres (no tenemos objetos aquí)
        if isinstance(seleccionados, set):
            for n in seleccionados:
                f.write(f"{n}\n")
        else:
            # lista de dicts con campos
            for p in seleccionados:
                f.write(f"{p['nombre']:<15} {p['costo']:<10} {p['volumen']:<10}\n")
        f.write("-" * 40 + "\n")
        f.write(f"Volumen total ocupado: {volumen_total}\n")
        f.write(f"Costo total: {costo_total}\n")
        f.write(f"Vector solución: {vector}\n")
        f.write("=" * 40 + "\n")

    print("Resultados guardados correctamente en archivo.")