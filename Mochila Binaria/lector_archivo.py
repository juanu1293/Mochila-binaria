# lector_archivo.py

def leer_datos(nombre_archivo):
    """
    Lee un archivo con el formato:
    Capacidad: valor
    Producto - Costo - Volumen

    Retorna una tupla (capacidad, productos)
    donde productos es una lista de diccionarios.
    """
    capacidad = None
    productos = []

    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()

        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue

            # Leer capacidad de la mochila
            if linea.lower().startswith("capacidad"):
                try:
                    capacidad = float(linea.split(":")[1].strip())
                except (IndexError, ValueError):
                    print("Error al leer la capacidad de la mochila.")
                continue

            # Leer productos
            partes = [p.strip() for p in linea.split('-')]
            if len(partes) != 3:
                print(f"Línea inválida (omitida): {linea}")
                continue

            nombre, costo, volumen = partes
            try:
                costo = float(costo)
                volumen = float(volumen)
            except ValueError:
                print(f"Error al convertir números en la línea: {linea}")
                continue

            productos.append({
                "nombre": nombre,
                "costo": costo,
                "volumen": volumen
            })

    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{nombre_archivo}'.")

    return  productos, capacidad


# Prueba básica
if __name__ == "__main__":
    cap, datos = leer_datos("productos.txt")
    print(f"Capacidad: {cap}")
    for p in datos:
        print(p)
