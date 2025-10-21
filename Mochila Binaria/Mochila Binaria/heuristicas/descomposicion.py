import os
from copy import deepcopy
from heuristicas.mayor_costo import heuristica_mayor_costo
from heuristicas.menor_volumen import heuristica_menor_volumen
from heuristicas.mayor_costo_volumen import heuristica_mayor_costo_volumen
from heuristicas.azar_const import heuristica_azar

def _guardar_resultados_global(seleccionados, volumen_total, costo_total, vector, capacidad_total):
    os.makedirs("resultados", exist_ok=True)
    ruta = os.path.join("resultados", "resultado_mochila.txt")
    with open(ruta, "a", encoding="utf-8") as f:
        f.write("\n=== RESULTADOS: Descomposición en sub-mochilas ===\n")
        f.write(f"Capacidad total original: {capacidad_total}\n")
        f.write(f"Volumen total ocupado (todas sub-mochilas): {volumen_total}\n")
        f.write(f"Costo total (todas sub-mochilas): {costo_total}\n")
        f.write(f"Vector solución global: {vector}\n")
        f.write("=" * 50 + "\n")

    print("Resultados de descomposición guardados correctamente en archivo.")


def heuristica_descomposicion(productos, capacidad_total):
    """
    Permite dividir la mochila en hasta 6 sub-mochilas.
    - El usuario indica cuántas (2..6).
    - Para cada sub-mochila se solicita una capacidad dentro de un rango válido.
    - El rango mínimo = volumen mínimo entre todos los productos.
    - El rango máximo se calcula para garantizar que las mochilas restantes puedan
      guardar (sin repetir) al menos los productos de menor volumen.
      Cálculo: max_i = capacidad_restante - sum(menores_volumenes[:k-i])
    - Para cada sub se asigna una heurística (Mayor costo, Menor volumen, Mayor costo/volumen, Azar).
    - Luego se resuelven las sub-mochilas en orden de menor capacidad a mayor, sin repetir productos.
    """
    if not productos:
        print("No hay productos cargados.")
        return None

    n_subs = 0
    while True:
        try:
            n_subs = int(input("Ingrese número de sub-mochilas a crear (2..6): "))
            if 2 <= n_subs <= 6:
                break
        except ValueError:
            pass
        print("Valor inválido. Ingrese un entero entre 2 y 6.")

    # preparar volúmenes ordenados (para cálculo de máximos conservadores)
    vols_sorted = sorted([p['volumen'] for p in productos])
    min_vol = vols_sorted[0]

    remaining_capacity = capacidad_total
    caps = []
    heuristicas = []

    opciones_heur = ["Mayor costo", "Menor volumen", "Mayor costo/volumen", "Azar"]
    print("\nHeurísticas disponibles por sub-mochila:")
    for i, o in enumerate(opciones_heur, 1):
        print(f"{i}. {o}")

    # solicitar capacidades y heurísticas secuencialmente (rango calculado por cada paso)
    for i in range(1, n_subs + 1):
        remaining_subs = n_subs - i
        # suma de los menores volúmenes para garantizar espacio a las subs restantes
        suma_menores = sum(vols_sorted[:remaining_subs]) if remaining_subs > 0 else 0
        max_i = remaining_capacity - suma_menores
        min_i = min_vol
        if max_i < min_i:
            # si por alguna razón no hay margen, forzar max = min
            max_i = min_i

        # solicitar capacidad para la sub-mochila i
        cap_i = None
        while True:
            try:
                entrada = input(f"Sub-mochila {i}/{n_subs} - ingrese capacidad (mín {min_i}, máx {max_i}, restante {remaining_capacity}): ").strip()
                cap_i = float(entrada)
                if min_i <= cap_i <= max_i:
                    break
            except ValueError:
                pass
            print("Capacidad inválida. Intente nuevamente dentro del rango indicado.")

        # solicitar heurística para esta sub
        heur_i = None
        while True:
            sel = input(f"Sub-mochila {i} - seleccione heurística (ingrese índice 1-{len(opciones_heur)}): ").strip()
            if sel.isdigit():
                idx = int(sel)
                if 1 <= idx <= len(opciones_heur):
                    heur_i = opciones_heur[idx - 1]
                    break
            print("Selección inválida. Intente nuevamente.")

        caps.append(cap_i)
        heuristicas.append(heur_i)
        remaining_capacity -= cap_i

    # validar que la suma de caps no excede la capacidad_total (debería ser válido por construcción)
    if sum(caps) - 1e-9 > capacidad_total:
        print("Error interno: suma de capacidades excede la capacidad total. Abortando.")
        return None

    # construir lista de sub-mochilas y resolver en orden de menor capacidad
    subs = []
    for idx, (c, h) in enumerate(zip(caps, heuristicas), start=1):
        subs.append({"id": idx, "capacidad": c, "heuristica": h})

    subs_sorted = sorted(subs, key=lambda x: x['capacidad'])

    productos_disponibles = deepcopy(productos)
    seleccionados_global = set()
    volumen_total_global = 0
    costo_total_global = 0

    # mapear nombre de heurística a función
    func_map = {
        "Mayor costo": heuristica_mayor_costo,
        "Menor volumen": heuristica_menor_volumen,
        "Mayor costo/volumen": heuristica_mayor_costo_volumen,
        "Azar": heuristica_azar
    }

    for s in subs_sorted:
        hname = s['heuristica']
        cap = s['capacidad']
        func = func_map.get(hname)
        if func is None:
            print(f"Heurística '{hname}' no implementada para sub-mochila. Se omite.")
            continue

        print(f"\n--- Resolviendo sub-mochila {s['id']} (cap {cap}, heurística: {hname}) ---")
        # llamar a la heurística con los productos disponibles
        resultado = func(productos_disponibles, cap)

        # resultado esperado contiene 'seleccionados' como lista de dicts y 'vector' relativo a productos_disponibles
        if not resultado:
            print(f"No se obtuvo resultado para sub-mochila {s['id']}.")
            continue

        # algunos heurísticos devuelven 'seleccionados' como lista de dicts; normalizar
        sel_items = resultado.get('seleccionados', [])
        nombres_sel = {p['nombre'] for p in sel_items}

        # remover items seleccionados de productos_disponibles
        productos_disponibles = [p for p in productos_disponibles if p['nombre'] not in nombres_sel]

        # acumular totales
        volumen_total_global += resultado.get('volumen_total', 0)
        costo_total_global += resultado.get('costo_total', 0)
        seleccionados_global.update(nombres_sel)

    # construir vector global con orden original de 'productos'
    vector_global = [1 if p['nombre'] in seleccionados_global else 0 for p in productos]

    # guardar resumen global
    _guardar_resultados_global(list(seleccionados_global), volumen_total_global, costo_total_global, vector_global, capacidad_total)

    return {
        'seleccionados': [p for p in productos if p['nombre'] in seleccionados_global],
        'volumen_total': volumen_total_global,
        'costo_total': costo_total_global,
        'vector': vector_global
    }