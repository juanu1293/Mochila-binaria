
print("Hello, World!bector , ")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mochila Binaria por Enfoque de Indicadores con Metaheurísticas
Requerimientos de práctica: permite ingreso manual, carga desde archivo CSV,
ejecución de heurísticas constructivas, de reducción y de descomposición,
configuración de combinaciones K1/K2, alternancia (hasta 3 heurísticas en orden),
semilla para procedimientos aleatorios, división en submochilas y asignación
de heurística por submochila. Muestra vector X, costo alcanzado y volumen usado,
indica la mejor solución entre las ejecutadas y registra resultados en TXT.
"""

import csv
import random
import os
import math
from datetime import datetime
from copy import deepcopy

REGISTRO = "registro_mochila.txt"

# ------------------------------
# UTILIDADES
# ------------------------------
def ahora(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def registrar(linea):
    with open(REGISTRO, "a", encoding="utf-8") as f:
        f.write(f"[{ahora()}] {linea}\n")

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

# ------------------------------
# CARGA / GUARDADO
# ------------------------------
def cargar_csv(path):
    C = []
    V = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        # Detect columns: try to find cost/volume names
        idx_c, idx_v = None, None
        for i,h in enumerate(headers):
            hlow = h.strip().lower()
            if hlow in ('c','ci','cost','costo','valor','beneficio'):
                idx_c = i
            if hlow in ('v','vi','vol','volumen','volume'):
                idx_v = i
        if idx_c is None or idx_v is None:
            # assume first two columns are cost and volume
            idx_c, idx_v = 0, 1
        for row in reader:
            try:
                c = float(row[idx_c])
                v = float(row[idx_v])
            except Exception:
                continue
            C.append(c); V.append(v)
    return C, V

def generar_dataset(n, path="dataset_ejemplo.csv", seed=None):
    if seed is not None:
        random.seed(seed)
    C = [round(random.uniform(1, 100), 2) for _ in range(n)]
    V = [round(random.uniform(1, 30), 2) for _ in range(n)]
    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Ci", "Vi"])
        for i in range(n):
            writer.writerow([C[i], V[i]])
    return C, V, path

# ------------------------------
# FUNCIONES BÁSICAS
# ------------------------------
def valor_y_volumen_por_X(X, C, V):
    z = sum(C[i]*X[i] for i in range(len(X)))
    vol = sum(V[i]*X[i] for i in range(len(X)))
    return z, vol

def X_desde_indices(indices, n):
    X = [0]*n
    for i in indices:
        if 0 <= i < n:
            X[i] = 1
    return X

def indices_desde_X(X):
    return [i for i,val in enumerate(X) if val==1]

# Programación dinámica (óptimo exacto) - devuelve Zopt y Xopt
def knapsack_dp(C, V, capacidad):
    W = int(capacidad)
    n = len(C)
    if W < 0:
        return 0, [0]*n
    dp = [[0]*(W+1) for _ in range(n+1)]
    for i in range(1, n+1):
        ci = int(C[i-1])
        vi = int(V[i-1])
        for w in range(W+1):
            if vi <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-vi] + ci)
            else:
                dp[i][w] = dp[i-1][w]
    Zopt = dp[n][W]
    Xopt = [0]*n
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            Xopt[i-1] = 1
            w -= int(V[i-1])
    return Zopt, Xopt

# ------------------------------
# HEURÍSTICAS CONSTRUCTIVAS (sensibilidad)
# Cada función devuelve (Z, volumen, indices_seleccionados)
# ------------------------------
def heur_mayor_costo(items, capacidad):
    datos = sorted(items, key=lambda x: x[1], reverse=True)
    sel = []; totc = 0; totv = 0
    for idx,c,v in datos:
        if totv + v <= capacidad:
            sel.append(idx); totc += c; totv += v
    return totc, totv, sel

def heur_menor_volumen(items, capacidad):
    datos = sorted(items, key=lambda x: x[2])
    sel=[]; totc=totv=0
    for idx,c,v in datos:
        if totv + v <= capacidad:
            sel.append(idx); totc += c; totv += v
    return totc, totv, sel

def heur_costo_volumen(items, capacidad):
    datos = sorted(items, key=lambda x: (x[1]/x[2]) if x[2] != 0 else float('inf'), reverse=True)
    sel=[]; totc=totv=0
    for idx,c,v in datos:
        if totv + v <= capacidad:
            sel.append(idx); totc += c; totv += v
    return totc, totv, sel

def heur_combinacion(items, capacidad, k1, k2):
    datos = sorted(items, key=lambda x: k1*x[1] + k2*x[2], reverse=True)
    sel=[]; totc=totv=0
    for idx,c,v in datos:
        if totv + v <= capacidad:
            sel.append(idx); totc += c; totv += v
    return totc, totv, sel

def heur_azar(items, capacidad, semilla=None):
    if semilla is not None:
        random.seed(semilla)
    datos = items[:]
    random.shuffle(datos)
    sel=[]; totc=totv=0
    for idx,c,v in datos:
        if totv + v <= capacidad:
            sel.append(idx); totc += c; totv += v
    return totc, totv, sel

# ------------------------------
# HEURÍSTICA REDUCTIVA
# Partir con todos e ir eliminando peor Ci/Vi hasta cumplir capacidad
# ------------------------------
def heur_reductiva(items, capacidad):
    sel = [idx for idx,_,_ in items]
    totc = sum(c for _,c,_ in items)
    totv = sum(v for _,_,v in items)
    if totv <= capacidad:
        return totc, totv, sel
    d = {idx:(c,v) for idx,c,v in items}
    while totv > capacidad and sel:
        peor = min(sel, key=lambda x: (d[x][0]/d[x][1]) if d[x][1]!=0 else float('inf'))
        c,v = d[peor]
        sel.remove(peor)
        totc -= c; totv -= v
    return totc, totv, sel

# ------------------------------
# ALTERNANCIA: hasta 3 heurísticas en un orden definido
# Implementación: aplicar heurísticas en el orden elegido, cada una intenta añadir
# objetos no seleccionados según su criterio hasta no poder añadir más; repetir una pasada
# ------------------------------
def heur_alternancia(items, capacidad, lista_heur_funcs, semilla=None):
    n = len(items)
    selected = set()
    totv = 0
    totc = 0
    items_by_idx = {idx:(c,v) for idx,c,v in items}
    # iterate heuristics in order one pass; can repeat cycles until no change (limit cycles)
    changed = True
    cycles = 0
    while changed and cycles < 5:
        changed = False
        cycles += 1
        for func in lista_heur_funcs:
            # construct list of remaining items for this heuristic in their order
            remaining = [(idx,c,v) for idx,c,v in items if idx not in selected]
            # apply heuristic's ordering by calling the heuristic on remaining with full capacity but we will filter by remaining capacity
            if func.__name__ == "heur_combinacion":
                # combinacion needs partial binding; assume caller provided a lambda bound with k1/k2
                Z,_,sel = func(remaining, capacidad - totv)
            else:
                Z,_,sel = func(remaining, capacidad - totv)
            # sel are indices relative to remaining list; we need to map to original indices because remaining contains original idx
            # In our heuristics, sel returns original indices already (we preserved idx), so we can use them directly
            for idx in sel:
                if idx not in selected:
                    c,v = items_by_idx[idx]
                    if totv + v <= capacidad:
                        selected.add(idx)
                        totv += v; totc += c
                        changed = True
    return totc, totv, sorted(selected)

# ------------------------------
# METAHEURÍSTICAS (mejoras sobre una solución inicial)
# Hill Climbing, Simulated Annealing, Genetic Algorithm, Tabu Search
# Cada recibe un vector X inicial (lista 0/1) y devuelve solución mejorada
# ------------------------------
def hill_climbing(X_init, C, V, capacidad, max_iters=1000):
    n = len(X_init)
    X = X_init[:]
    bestZ, bestV = valor_y_volumen_por_X(X, C, V)
    it = 0
    improved = True
    while improved and it < max_iters:
        improved = False
        it += 1
        for i in range(n):
            Xn = X[:]; Xn[i] = 1 - Xn[i]
            z, vol = valor_y_volumen_por_X(Xn, C, V)
            if vol <= capacidad and z > bestZ:
                X = Xn; bestZ = z; bestV = vol; improved = True
                break
    return bestZ, bestV, indices_desde_X(X), X

def simulated_annealing(X_init, C, V, capacidad, T0=100.0, alpha=0.95, max_iters=1000, seed=None):
    if seed is not None: random.seed(seed)
    n = len(X_init)
    current = X_init[:]
    curZ, curV = valor_y_volumen_por_X(current, C, V)
    best = current[:]; bestZ = curZ; bestV = curV
    T = T0
    for t in range(max_iters):
        i = random.randrange(n)
        neigh = current[:]; neigh[i] = 1 - neigh[i]
        z, vol = valor_y_volumen_por_X(neigh, C, V)
        if vol <= capacidad:
            delta = z - curZ
            if delta > 0 or random.random() < math.exp(delta / max(1e-12, T)):
                current = neigh; curZ = z; curV = vol
                if curZ > bestZ:
                    best = current[:]; bestZ = curZ; bestV = curV
        T *= alpha
        if T < 1e-8:
            break
    return bestZ, bestV, indices_desde_X(best), best

def genetic_algorithm(C, V, capacidad, pop_size=50, generations=100, crossover_p=0.8, mutation_p=0.05, seed=None):
    if seed is not None: random.seed(seed)
    n = len(C)
    def random_sol():
        X = [0]*n
        for i in range(n):
            if random.random() < 0.3:
                X[i] = 1
        # fix volume
        while sum(V[i]*X[i] for i in range(n)) > capacidad:
            ones = [i for i in range(n) if X[i]==1]
            if not ones: break
            X[random.choice(ones)] = 0
        return X
    def fitness(X):
        return sum(C[i]*X[i] for i in range(n))
    pop = [random_sol() for _ in range(pop_size)]
    best = (fitness(pop[0]), pop[0])
    for g in range(generations):
        scored = [(fitness(ind), ind) for ind in pop]
        scored.sort(key=lambda x: x[0], reverse=True)
        if scored[0][0] > best[0]: best = scored[0]
        newpop = [scored[0][1][:], scored[1][1][:]]  # elitism
        while len(newpop) < pop_size:
            a = random.choice(scored)[1]; b = random.choice(scored)[1]
            p1 = a if fitness(a) > fitness(b) else b
            c = random.choice(scored)[1]; d = random.choice(scored)[1]
            p2 = c if fitness(c) > fitness(d) else d
            child1 = p1[:]; child2 = p2[:]
            if random.random() < crossover_p:
                pt = random.randint(1, n-1)
                child1 = p1[:pt] + p2[pt:]
                child2 = p2[:pt] + p1[pt:]
            for child in (child1, child2):
                for i in range(n):
                    if random.random() < mutation_p:
                        child[i] = 1 - child[i]
                # fix volume
                while sum(V[i]*child[i] for i in range(n)) > capacidad:
                    ones = [i for i in range(n) if child[i]==1]
                    if not ones: break
                    child[random.choice(ones)] = 0
                newpop.append(child)
                if len(newpop) >= pop_size: break
        pop = newpop[:pop_size]
    bestX = best[1]
    bestZ = fitness(bestX)
    bestV = sum(V[i]*bestX[i] for i in range(n))
    return bestZ, bestV, indices_desde_X(bestX), bestX

def tabu_search(X_init, C, V, capacidad, tenure=7, max_iters=200):
    n = len(X_init)
    current = X_init[:]
    curZ, curV = valor_y_volumen_por_X(current, C, V)
    best = current[:]; bestZ = curZ; bestV = curV
    tabu = {}
    it = 0
    while it < max_iters:
        it += 1
        neighbors = []
        for i in range(n):
            neigh = current[:]; neigh[i] = 1 - neigh[i]
            z, vol = valor_y_volumen_por_X(neigh, C, V)
            if vol <= capacidad:
                neighbors.append((z, i, neigh))
        if not neighbors: break
        neighbors.sort(key=lambda x: x[0], reverse=True)
        chosen = None
        for z, i, neigh in neighbors:
            if i not in tabu or z > bestZ:
                chosen = (z, i, neigh); break
        if chosen is None: break
        z, i, neigh = chosen
        current = neigh; curZ = z
        tabu = {k: v-1 for k,v in tabu.items() if v-1>0}
        tabu[i] = tenure
        if curZ > bestZ:
            bestZ = curZ; best = current[:]
    bestV = sum(V[i]*best[i] for i in range(n))
    return bestZ, bestV, indices_desde_X(best), best

# ------------------------------
# DESCOMPOSICIÓN: dividir mochila en submochilas y asignar heurística por submochila
# Para cada submochila se ejecuta la heurística elegida sobre items NO asignados aún (secuencial)
# ------------------------------
def descomposicion_secuencial(items, subcaps, heur_por_sub, C, V, semilla=None):
    # items: list of (idx,ci,vi)
    items_dict = {idx:(ci,vi) for idx,ci,vi in items}
    asignaciones = []  # per submochila: (indices_selected, Z, vol)
    disponibles = set(idx for idx,_,_ in items)
    random.seed(semilla)
    for s,cap in enumerate(subcaps):
        heur = heur_por_sub[s]  # a callable that takes (items_subset, cap) and returns (Z,vol,sel)
        subset = [(idx, items_dict[idx][0], items_dict[idx][1]) for idx in items if idx in disponibles]
        Z, vol, sel = heur(subset, cap)
        # sel contains original indices
        asignaciones.append((sel, Z, vol))
        for idx in sel:
            if idx in disponibles:
                disponibles.remove(idx)
    # summary
    totalZ = sum(a[1] for a in asignaciones)
    totalVol = sum(a[2] for a in asignaciones)
    chosen = [idx for a in asignaciones for idx in a[0]]
    return asignaciones, totalZ, totalVol, chosen

# ------------------------------
# INTERFAZ CONSOLA (MENÚ PRINCIPAL)
# ------------------------------
def menu_principal():
    limpiar()
    print("Mochila binaria - Metaheurísticas por enfoque de indicadores")
    C = []; V = []; items = []; capacidad = 0
    semilla_global = None
    while True:
        print("\nMenú principal:")
        print("1) Ingresar items manualmente")
        print("2) Cargar items desde CSV")
        print("3) Generar dataset de prueba (50-100 ítems) y guardar CSV")
        print("4) Configurar semilla (procedimientos aleatorios)")
        print("5) Ejecutar metaheurística (Constructivas / Reducción / Descomposición)")
        print("6) Mostrar registro (archivo registro_mochila.txt)")
        print("7) Salir")
        op = input("Opción: ").strip()
        if op == "1":
            try:
                n = int(input("Número de ítems: "))
                C=[]; V=[]
                for i in range(n):
                    ci = float(input(f" Ci para ítem {i+1}: "))
                    vi = float(input(f" Vi para ítem {i+1}: "))
                    C.append(ci); V.append(vi)
                capacidad = float(input("Capacidad total de la mochila: "))
                items = [(i, C[i], V[i]) for i in range(len(C))]
                print("Datos cargados en memoria.")
            except Exception as e:
                print("Entrada inválida:", e)
        elif op == "2":
            path = input("Ruta CSV (ej: items.csv): ").strip()
            try:
                C, V = cargar_csv(path)
                items = [(i, C[i], V[i]) for i in range(len(C))]
                capacidad = float(input("Capacidad total de la mochila: "))
                print(f"Cargados {len(C)} ítems.")
            except Exception as e:
                print("Error cargando CSV:", e)
        elif op == "3":
            try:
                n = int(input("Tamaño (50-100 recomendado): "))
                seed = input("Semilla opcional para generación (ENTER para aleatorio): ").strip()
                seedv = int(seed) if seed else None
                C, V, ruta = generar_dataset(n)
                items = [(i, C[i], V[i]) for i in range(len(C))]
                capacidad = float(input("Capacidad total de la mochila (ej 500): "))
                print(f"Dataset generado y guardado en {ruta}")
            except Exception as e:
                print("Error generando dataset:", e)
        elif op == "4":
            s = input("Ingrese semilla entera (ENTER para quitar): ").strip()
            semilla_global = int(s) if s else None
            print("Semilla global ajustada a:", semilla_global)
        elif op == "5":
            if not items:
                print("Primero cargue o ingrese items (opciones 1-3)."); continue
            ejecutar_metaheuristica(items, capacidad, C, V, semilla_global)
        elif op == "6":
            if os.path.exists(REGISTRO):
                with open(REGISTRO, "r", encoding="utf-8") as f:
                    print(f.read())
            else:
                print("No existe archivo de registro aún.")
        elif op == "7":
            print("Saliendo..."); break
        else:
            print("Opción inválida.")

# ------------------------------
# FLUJO PRINCIPAL PARA EJECUTAR METAHEURÍSTICA SEGÚN ESPECIFICACIÓN
# ------------------------------
def ejecutar_metaheuristica(items, capacidad, C, V, semilla_global=None):
    limpiar()
    print("Seleccione tipo de metaheurística a aplicar:")
    print("1) Constructivas (varias heurísticas de sensibilidad)")
    print("2) Reducción (heurística reductiva)")
    print("3) Descomposición (dividir mochila en submochilas)")
    tipo = input("Opción (1/2/3): ").strip()
    resultados = []  # lista de dicts con resultados por heurística
    items_map = {idx:(c,v) for idx,c,v in items}
    if tipo == "1":
        # list all constructiva heuristics and allow multiple selection
        print("\nHeurísticas constructivas disponibles:")
        print("1) Mayor Costo")
        print("2) Menor Volumen")
        print("3) Costo/Volumen")
        print("4) Combinación lineal (K1,K2) - permite múltiples combinaciones")
        print("5) Azar (procedimiento aleatorio, requiere semilla)")
        sel = input("Ingrese números separados por coma de las heurísticas a ejecutar (ej: 1,3,4): ").strip()
        choices = [s.strip() for s in sel.split(",") if s.strip()]
        heur_elegidas = []
        combinaciones = []
        seed_for_random = semilla_global
        for c in choices:
            if c == "1":
                heur_elegidas.append(("Mayor Costo", heur_mayor_costo))
            elif c == "2":
                heur_elegidas.append(("Menor Volumen", heur_menor_volumen))
            elif c == "3":
                heur_elegidas.append(("Costo/Volumen", heur_costo_volumen))
            elif c == "4":
                kcount = int(input("¿Cuántas combinaciones (pares K1,K2) desea probar?: "))
                for i in range(kcount):
                    k1 = float(input(f" K1 para combinación {i+1}: "))
                    k2 = float(input(f" K2 para combinación {i+1}: "))
                    # create a lambda that binds k1,k2 and works on an items list with same signature
                    heur_func = lambda its,cap, k1=k1, k2=k2: heur_combinacion(its, cap, k1, k2)
                    name = f"Combinación (K1={k1},K2={k2})"
                    heur_elegidas.append((name, heur_func))
            elif c == "5":
                s = input("Semilla para heurística azar (ENTER para usar semilla global o aleatoria): ").strip()
                seed_for_random = int(s) if s else semilla_global
                heur_elegidas.append(("Azar", lambda its,cap, seed=seed_for_random: heur_azar(its, cap, seed)))
            else:
                print("Opción inválida:", c)
        # Alternancia: user may choose alternation among up to 3 heuristics
        print("\n¿Desea usar alternancia (aplicar en orden hasta 3 heurísticas)?")
        altq = input("Responder s/n: ").strip().lower()
        if altq == "s":
            print("Seleccione hasta 3 heurísticas para alternar (por índice como antes).")
            print("Reutilice los índices de heurísticas constructivas: 1,2,3,4,5")
            order = input("Ingrese la secuencia separada por comas (ej: 3,1,2): ").strip()
            seq = [s.strip() for s in order.split(",") if s.strip()][:3]
            # build list of functions corresponding to chosen order
            func_order = []
            for code in seq:
                if code == "1": func_order.append(heur_mayor_costo)
                elif code == "2": func_order.append(heur_menor_volumen)
                elif code == "3": func_order.append(heur_costo_volumen)
                elif code == "4":
                    k1 = float(input(" K1 para combinacion en alternancia: "))
                    k2 = float(input(" K2 para combinacion en alternancia: "))
                    func_order.append(lambda its,cap, k1=k1, k2=k2: heur_combinacion(its, cap, k1, k2))
                elif code == "5":
                    s = input(" Semilla para alternancia-azar (ENTER para global): ").strip()
                    seed_a = int(s) if s else semilla_global
                    func_order.append(lambda its,cap, seed=seed_a: heur_azar(its, cap, seed))
                else:
                    print("Código inválido en alternancia:", code)
            # execute alternancia
            Z, vol, sel = heur_alternancia(items, capacidad, func_order, semilla_global)
            X = X_desde_indices(sel, len(C))
            Zopt, Xopt = knapsack_dp(C, V, capacidad)
            resultados.append({"metodo":"Alternancia", "X":X, "Z":Z, "vol":vol, "info":f"Orden: {seq}"})
            print("\nResultado Alternancia:")
            print(f" Z={Z:.2f}, Volumen={vol:.2f}, Items seleccionados={['X'+str(i+1) for i in sel]}")
            print(f" Óptimo (DP) = {Zopt}")
            registrar(f"Alternancia Z={Z:.2f} Vol={vol:.2f} Orden={seq}")
        # execute each chosen heuristica (if alternancia used, still execute individual ones as well)
        for name, func in heur_elegidas:
            # func signature: (items_subset, capacidad_sub) -> (Z,vol,sel)
            try:
                Z, vol, sel = func(items, capacidad)
            except TypeError:
                # support heuristics implemented with different signature
                Z, vol, sel = func(items, capacidad)
            X = X_desde_indices(sel, len(C))
            resultados.append({"metodo": name, "X":X, "Z":Z, "vol":vol, "info": ""})
            print(f"\n{name}: Z={Z:.2f}, Vol={vol:.2f}, seleccionados={len(sel)}")
            registrar(f"{name} Z={Z:.2f} Vol={vol:.2f} Seleccionados={len(sel)}")
    elif tipo == "2":
        # Reducción: allow user to run the reductive heuristic and optionally combine with other heuristics
        print("\nEjecutando heurística reductiva (partir con todos y eliminar los menos rentables)...")
        Z, vol, sel = heur_reductiva(items, capacidad)
        X = X_desde_indices(sel, len(C))
        Zopt, Xopt = knapsack_dp(C, V, capacidad)
        resultados.append({"metodo":"Reductiva", "X":X, "Z":Z, "vol":vol, "info":""})
        print(f"Reductiva: Z={Z:.2f}, Vol={vol:.2f}, Items={len(sel)}")
        registrar(f"Reductiva Z={Z:.2f} Vol={vol:.2f} Items={len(sel)}")
    elif tipo == "3":
        # Descomposición: ask for number of submochilas and capacities
        try:
            k = int(input("¿En cuántas partes desea dividir la mochila? (entero>=1): "))
            subcaps = []
            suma = 0.0
            for i in range(k):
                cap_i = float(input(f" Capacidad submochila {i+1}: "))
                subcaps.append(cap_i); suma += cap_i
            if abs(suma - capacidad) > 1e-6:
                print("Advertencia: la suma de subcapacidades no coincide con la capacidad total.")
            heur_por_sub = []
            print("\nPara cada submochila elija una heurística de sensibilidad (por índice):")
            for i in range(k):
                print(f" Submochila {i+1}:")
                print(" 1) Mayor Costo  2) Menor Volumen  3) Costo/Volumen  4) Combinación (K1,K2)  5) Azar")
                code = input(" Seleccione código: ").strip()
                if code == "1":
                    heur_por_sub.append(heur_mayor_costo)
                elif code == "2":
                    heur_por_sub.append(heur_menor_volumen)
                elif code == "3":
                    heur_por_sub.append(heur_costo_volumen)
                elif code == "4":
                    k1 = float(input("  Ingrese K1: ")); k2 = float(input("  Ingrese K2: "))
                    heur_por_sub.append(lambda its, cap, k1=k1, k2=k2: heur_combinacion(its, cap, k1, k2))
                elif code == "5":
                    s = input("  Semilla para azar (ENTER para global): ").strip()
                    sseed = int(s) if s else semilla_global
                    heur_por_sub.append(lambda its, cap, sseed=sseed: heur_azar(its, cap, sseed))
                else:
                    print("  Código inválido, se usará Mayor Costo por defecto.")
                    heur_por_sub.append(heur_mayor_costo)
            asign, totalZ, totalVol, chosen = descomposicion_secuencial(items, subcaps, heur_por_sub, C, V, semilla_global)
            resultados.append({"metodo":"Descomposición", "X": X_desde_indices(chosen, len(C)), "Z":totalZ, "vol":totalVol, "info":f"Subcaps={subcaps}"})
            print("\nResultado Descomposición:")
            for i,(sel_i, Zi, voli) in enumerate(asign):
                print(f" Submochila {i+1}: Z={Zi:.2f}, Vol={voli:.2f}, Items={['X'+str(x+1) for x in sel_i]}")
            print(f" Total Z={totalZ:.2f}, Total Vol={totalVol:.2f}")
            registrar(f"Descomposicion TotalZ={totalZ:.2f} TotalVol={totalVol:.2f} Subcaps={subcaps}")
        except Exception as e:
            print("Error en descomposición:", e)
            return
    else:
        print("Opción inválida.")
        return

    # Al final: mostrar resumen de todas las heurísticas ejecutadas y elegir la mejor solución por Z
    if resultados:
        mejor = max(resultados, key=lambda r: r["Z"])
        Zopt, Xopt = knapsack_dp(C, V, capacidad)
        print("\n--- Resumen de soluciones ejecutadas ---")
        print(f"{'Método':35} {'Z':>10} {'Vol':>10} {'#items':>8}")
        for r in resultados:
            xi = r.get("X", None)
            cnt = sum(1 for v in xi if v==1) if xi else 0
            print(f"{r['metodo'][:35]:35} {r['Z']:10.2f} {r['vol']:10.2f} {cnt:8d}")
        print("-"*70)
        print(f"Óptimo exacto (DP) = {Zopt}")
        print(f"Mejor solución: {mejor['metodo']} -> Z={mejor['Z']:.2f}, Vol={mejor['vol']:.2f}")
        # Mostrar vector y detalles de mejor
        Xbest = mejor.get("X", None)
        if Xbest:
            sel_idx = indices_desde_X(Xbest)
            print(f"Vector X (mejor): {Xbest}")
            print(f"Ítems seleccionados: {['X'+str(i+1) for i in sel_idx]}")
        registrar(f"Resumen Ejecutadas Mejor:{mejor['metodo']} Z={mejor['Z']:.2f} Vol={mejor['vol']:.2f}")
    else:
        print("No se ejecutó ninguna heurística.")

# ------------------------------
# EJECUTAR APLICACIÓN
# ------------------------------
if __name__ == "__main__":
    menu_principal()