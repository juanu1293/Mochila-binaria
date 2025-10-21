import random

def ejecutar_rand(productos, capacidad, parametros):
    """
    Heurística de Azar (eliminación aleatoria):
    - Inicia con todos los productos.
    - Elimina productos aleatoriamente hasta que el volumen total <= capacidad.
    - Muestra y guarda el orden de eliminación y la solución final.
    """

    raiz = parametros.get("raiz", None)
    if raiz is not None:
        random.seed(raiz)
        print(f"Usando semilla: {raiz}")
    else:
        random.seed()

    # Copiar lista de productos inicial
    seleccionados = productos[:]
    random.shuffle(seleccionados)

    # Calcular volumen y costo total inicial
    volumen_total = sum(p["volumen"] for p in seleccionados)
    costo_total = sum(p["costo"] for p in seleccionados)
    eliminados = []

    # Eliminar productos al azar hasta estar por debajo o igual a la capacidad
    while volumen_total > capacidad and seleccionados:
        eliminado = random.choice(seleccionados)
        seleccionados.remove(eliminado)
        eliminados.append(eliminado["nombre"])
        volumen_total -= eliminado["volumen"]
        costo_total -= eliminado["costo"]

    # Crear vector solución
    nombres_sel = {p['nombre'] for p in seleccionados}
    vector_solucion = [1 if p['nombre'] in nombres_sel else 0 for p in productos]

    # === Mostrar resultados ===
    print("\n=== RESULTADOS: Heurística Azar ===")
    if eliminados:
        print("Orden de eliminación aleatoria:")
        for idx, nombre in enumerate(eliminados, 1):
            print(f"{idx}. {nombre}")
    else:
        print("No se eliminaron productos (ya estaba dentro del límite).")

    print("\nProductos finales seleccionados:")
    print(f"{'Producto':<15}{'Costo':<10}{'Volumen':<10}")
    print("-" * 40)
    for p in seleccionados:
        print(f"{p['nombre']:<15}{p['costo']:<10}{p['volumen']:<10}")
    print("-" * 40)
    print(f"Volumen total ocupado: {volumen_total}")
    print(f"Costo total: {costo_total}")
    print(f"Vector solución: {vector_solucion}")

    # === Guardar resultados en archivo ===
    with open("resultados.txt", "a", encoding="utf-8") as f:
        f.write("=== RESULTADOS: Heurística Azar ===\n")
        if raiz is not None:
            f.write(f"Semilla usada: {raiz}\n")
        if eliminados:
            f.write("Orden de eliminación aleatoria:\n")
            for idx, nombre in enumerate(eliminados, 1):
                f.write(f"{idx}. {nombre}\n")
        else:
            f.write("No se eliminaron productos (ya estaba dentro del límite).\n")

        f.write("\nProductos finales seleccionados:\n")
        f.write(f"{'Producto':<15}{'Costo':<10}{'Volumen':<10}\n")
        f.write("-" * 40 + "\n")
        for p in seleccionados:
            f.write(f"{p['nombre']:<15}{p['costo']:<10}{p['volumen']:<10}\n")
        f.write("-" * 40 + "\n")
        f.write(f"Volumen total ocupado: {volumen_total}\n")
        f.write(f"Costo total: {costo_total}\n")
        f.write(f"Vector solución: {vector_solucion}\n\n")

    # === Retornar resultado estándar ===
    return {
        'seleccionados': seleccionados,
        'volumen_total': volumen_total,
        'costo_total': costo_total,
        'vector': vector_solucion
    }
