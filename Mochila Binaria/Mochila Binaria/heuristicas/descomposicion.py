import os
from copy import deepcopy

from heuristicas.mayor_costo import heuristica_mayor_costo
from heuristicas.menor_volumen import heuristica_menor_volumen
from heuristicas.mayor_costo_volumen import heuristica_mayor_costo_volumen
from heuristicas.azar_const import heuristica_azar
from heuristicas.menor_cap_residual import heuristica_menor_cap_residual_libre
from heuristicas.heuristica_mayor_combinacion_lineal import heuristica_mayor_combinacion_lineal
from heuristicas.heuristica_azar import ejecutar_rand
from heuristicas.heuristica_mayor_volumen import ejecutar_vol
from heuristicas.heuristica_menor_combinacion_lineal import ejecutar_combinacion
from heuristicas.heuristica_menor_costo_volumen import ejecutar_costo_volumen
from heuristicas.heuristica_menor_costo import ejecutar_costo
from heuristicas.alternancia_const import heuristica_alternancia_constructiva
from heuristicas.alternancia_redu import heuristica_alternancia_reduccion


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
    Divide la mochila en 2..6 sub-mochilas. Para cada sub:
    - solicita capacidad (excepto la última: toma lo que sobra)
    - solicita heurística a usar (varias opciones, constructivas y de reducción)
    Resuelve las sub-mochilas en orden de menor a mayor capacidad y evita repetir productos.
    """
    if not productos:
        print("No hay productos cargados.")
        return None

    # solicitar número de sub-mochilas
    while True:
        try:
            n_subs = int(input("Ingrese número de sub-mochilas a crear (2..6): ").strip())
            if 2 <= n_subs <= 6:
                break
        except Exception:
            pass
        print("Valor inválido. Ingrese un entero entre 2 y 6.")

    # preparar volúmenes ordenados para cálculos de mínimos/máximos
    vols_sorted = sorted([p['volumen'] for p in productos])
    min_vol = vols_sorted[0] if vols_sorted else 0

    remaining_capacity = float(capacidad_total)
    caps = []
    heuristicas = []

    # Opciones ampliadas: constructivas y de reducción, listadas para que el usuario elija
    opciones_heur = [
        "Mayor costo (Constructiva)",
        "Menor volumen (Constructiva)",
        "Mayor combinación lineal (Constructiva)",
        "Mayor costo/volumen (Constructiva)",
        "Azar (Constructiva)",
        "Alternancia (Constructiva)",
        "Menor capacidad residual libre (Constructiva)",
        "Menor costo (Reducción)",
        "Mayor volumen (Reducción)",
        "Menor combinación lineal (Reducción)",
        "Menor costo/volumen (Reducción)",
        "Azar (Reducción)",
        "Alternancia (Reducción)"
    ]

    print("\nHeurísticas disponibles por sub-mochila:")
    for i, o in enumerate(opciones_heur, 1):
        print(f"{i}. {o}")

    # solicitar capacidades y heurísticas secuencialmente; última sub toma el restante automáticamente
    for i in range(1, n_subs + 1):
        remaining_subs = n_subs - i
        suma_menores = sum(vols_sorted[:remaining_subs]) if remaining_subs > 0 else 0
        max_i = remaining_capacity - suma_menores
        min_i = min_vol if min_vol > 0 else 0.0
        if max_i < min_i:
            max_i = min_i

        # última sub-mochila: asignar lo que sobra (no preguntar)
        if i == n_subs:
            cap_i = remaining_capacity
            print(f"Sub-mochila {i}/{n_subs} - capacidad asignada automáticamente: {cap_i}")
            # si por inconsistencia es menor que el mínimo, forzar mínimo
            if cap_i < min_i:
                print(f"Advertencia: capacidad restante ({cap_i}) menor que mínimo esperado ({min_i}). Se fuerza mínimo.")
                cap_i = min_i
            # tampoco debe exceder el máximo calculado (por seguridad)
            if cap_i > max_i:
                cap_i = max_i
        else:
            cap_i = None
            while True:
                try:
                    entrada = input(f"Sub-mochila {i}/{n_subs} - ingrese capacidad (mín {min_i}, máx {max_i}, restante {remaining_capacity}): ").strip()
                    cap_i = float(entrada)
                    if min_i <= cap_i <= max_i:
                        break
                except Exception:
                    pass
                print("Capacidad inválida. Intente nuevamente dentro del rango indicado.")

        # solicitar heurística para esta sub-mochila
        heur_i = None
        while True:
            sel = input(f"Sub-mochila {i} - seleccione heurística (ingrese índice 1-{len(opciones_heur)}): ").strip()
            if sel.isdigit():
                idx = int(sel)
                if 1 <= idx <= len(opciones_heur):
                    heur_i = opciones_heur[idx - 1]
                    break
            print("Selección inválida. Intente nuevamente.")

        caps.append(float(cap_i))
        heuristicas.append(heur_i)
        remaining_capacity -= float(cap_i)

    # comprobación final simple
    if sum(caps) - 1e-9 > capacidad_total:
        print("Error interno: suma de capacidades excede la capacidad total. Abortando.")
        return None

    # crear lista de sub-mochilas y ordenar por capacidad (menor a mayor)
    subs = [{"id": idx + 1, "capacidad": c, "heuristica": h} for idx, (c, h) in enumerate(zip(caps, heuristicas))]
    subs_sorted = sorted(subs, key=lambda x: x['capacidad'])

    productos_disponibles = deepcopy(productos)
    seleccionados_global = set()
    volumen_total_global = 0
    costo_total_global = 0

    # mapeo de nombres de heurística a funciones (preparado para futuras funciones)
    func_map = {
        "Mayor costo (Constructiva)": heuristica_mayor_costo,
        "Menor volumen (Constructiva)": heuristica_menor_volumen,
        "Mayor combinación lineal (Constructiva)": heuristica_mayor_combinacion_lineal,
        "Mayor costo/volumen (Constructiva)": heuristica_mayor_costo_volumen,
        "Azar (Constructiva)": heuristica_azar,
        "Alternancia (Constructiva)": heuristica_alternancia_constructiva,
        "Menor capacidad residual libre (Constructiva)": heuristica_menor_cap_residual_libre,
        "Menor costo (Reducción)": ejecutar_costo,
        "Mayor volumen (Reducción)": ejecutar_vol,
        "Menor combinación lineal (Reducción)": ejecutar_combinacion,
        "Menor costo/volumen (Reducción)": ejecutar_costo_volumen,
        "Azar (Reducción)": ejecutar_rand,
        "Alternancia (Reducción)": heuristica_alternancia_reduccion
    }

    # resolver cada sub-mochila
    for s in subs_sorted:
        hname = s['heuristica']
        cap = s['capacidad']
        func = func_map.get(hname)
        if func is None:
            print(f"Heurística '{hname}' no implementada para sub-mochila. Se omite.")
            continue

        print(f"\n--- Resolviendo sub-mochila {s['id']} (cap {cap}, heurística: {hname}) ---")
        resultado = func(productos_disponibles, cap)

        if not resultado:
            print(f"No se obtuvo resultado para sub-mochila {s['id']}.")
            continue

        sel_items = resultado.get('seleccionados', [])
        nombres_sel = {p['nombre'] for p in sel_items}

        # eliminar seleccionados de disponibles
        productos_disponibles = [p for p in productos_disponibles if p['nombre'] not in nombres_sel]

        volumen_total_global += resultado.get('volumen_total', 0)
        costo_total_global += resultado.get('costo_total', 0)
        seleccionados_global.update(nombres_sel)

    # vector global con el orden original de productos
    vector_global = [1 if p['nombre'] in seleccionados_global else 0 for p in productos]

    _guardar_resultados_global(list(seleccionados_global), volumen_total_global, costo_total_global, vector_global, capacidad_total)

    return {
        'seleccionados': [p for p in productos if p['nombre'] in seleccionados_global],
        'volumen_total': volumen_total_global,
        'costo_total': costo_total_global,
        'vector': vector_global
    }