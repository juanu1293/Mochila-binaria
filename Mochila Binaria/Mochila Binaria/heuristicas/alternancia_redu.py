import os
import random

def heuristica_alternancia_reduccion(productos, capacidad):
    """
    Heurística alternancia - de reducción.
    Parte de la solución completa (todos los ítems seleccionados) y alterna heurísticas
    de eliminación hasta que la solución respete la capacidad.

    Heurísticas base soportadas: 'Menor costo', 'Mayor volumen', 'Menos costo/volumen', 'Azar'
    """
    print("\n=== Alternancia (Reducción) ===")
    print("Puede elegir hasta 3 heurísticas de reducción a alternar en el orden deseado.")
    opciones = ['Menor costo', 'Mayor volumen', 'Menos costo/volumen', 'Azar']
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
        print("No se seleccionó heurística válida. Usando 'Mayor volumen' por defecto.")
        heur_sel = ['Mayor volumen']

    seed = None
    if 'Azar' in heur_sel:
        try:
            seed = int(input("Ingrese semilla para heurística 'Azar' (entero): "))
        except ValueError:
            seed = 0
        random.seed(seed)

    # iniciar con todos seleccionados
    seleccionados = {p['nombre'] for p in productos}
    volumen_total = sum(p['volumen'] for p in productos)
    costo_total = sum(p['costo'] for p in productos)

    # si ya cumple, no hacer nada
    if volumen_total <= capacidad:
        vector = [1 for _ in productos]
        guardar_resultados(seleccionados, volumen_total, costo_total, vector, capacidad, 'Alternancia-Redu', seed)
        return {
            'seleccionados': productos.copy(),
            'volumen_total': volumen_total,
            'costo_total': costo_total,
            'vector': vector,
            'semilla': seed
        }

    # función para elegir item a eliminar según heurística
    def elegir_a_eliminar(h, disponibles):
        lista = [p for p in productos if p['nombre'] in disponibles]
        if not lista:
            return None
        if h == 'Menor costo':
            return min(lista, key=lambda x: x['costo'])
        if h == 'Mayor volumen':
            return max(lista, key=lambda x: x['volumen'])
        if h == 'Menos costo/volumen':
            return min(lista, key=lambda x: (x['costo'] / x['volumen'] if x['volumen'] > 0 else float('inf')))
        if h == 'Azar':
            return random.choice(lista)
        return max(lista, key=lambda x: x['volumen'])

    # alternar heurísticas eliminando hasta cumplir capacidad
    while volumen_total > capacidad and seleccionados:
        for h in heur_sel:
            if volumen_total <= capacidad:
                break
            a_eliminar = elegir_a_eliminar(h, seleccionados)
            if not a_eliminar:
                continue
            seleccionados.remove(a_eliminar['nombre'])
            volumen_total -= a_eliminar['volumen']
            costo_total -= a_eliminar['costo']

    vector = [1 if p['nombre'] in seleccionados else 0 for p in productos]
    seleccionados_list = [p for p in productos if p['nombre'] in seleccionados]

    print("\n=== RESULTADOS: Alternancia (Reducción) ===")
    print(f"Heurísticas alternadas: {heur_sel}")
    print(f"Volumen total ocupado: {volumen_total}")
    print(f"Costo total: {costo_total}")
    print(f"Vector solución: {vector}")

    guardar_resultados(seleccionados, volumen_total, costo_total, vector, capacidad, 'Alternancia-Redu', seed)

    return {
        'seleccionados': seleccionados_list,
        'volumen_total': volumen_total,
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
        if isinstance(seleccionados, set):
            for n in seleccionados:
                f.write(f"{n}\n")
        else:
            for p in seleccionados:
                f.write(f"{p['nombre']:<15} {p['costo']:<10} {p['volumen']:<10}\n")
        f.write("-" * 40 + "\n")
        f.write(f"Volumen total ocupado: {volumen_total}\n")
        f.write(f"Costo total: {costo_total}\n")
        f.write(f"Vector solución: {vector}\n")
        f.write("=" * 40 + "\n")

    print("Resultados guardados correctamente en archivo.")