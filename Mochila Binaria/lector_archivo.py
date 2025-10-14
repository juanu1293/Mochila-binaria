# lector_archivo.py

def leer_productos(nombre_archivo):
    """
    Lee un archivo de texto con formato:
    Producto - Costo - Volumen
    y devuelve una lista de diccionarios.
    """
    productos = []

    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:  # Ignorar líneas vacías
                    continue

                # Separar los datos por el guion
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

    return productos


