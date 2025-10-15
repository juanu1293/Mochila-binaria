import random
import time
import matplotlib.pyplot as plt

# =============================
# LECTOR DE ARCHIVO
# =============================
def leer_productos(archivo):
    productos = []
    try:
        with open(archivo, 'r') as f:
            for linea in f:
                if linea.strip():
                    partes = [x.strip() for x in linea.strip().split('-')]
                    if len(partes) == 3:
                        productos.append({
                            'nombre': partes[0],
                            'costo': float(partes[1]),
                            'volumen': float(partes[2])
                        })
        print(f"{len(productos)} productos cargados.")
        return productos
    except Exception as e:
        print(f"Error al leer archivo: {e}")
        return []

# =============================
# GRÁFICA DINÁMICA
# =============================
class GraficaDinamica:
    def __init__(self, titulo):
        self.titulo = titulo
        self.valores = []
        self.fig, self.ax = plt.subplots()
        self.ax.set_title(titulo)
        self.ax.set_xlabel("Productos seleccionados")
        self.ax.set_ylabel("Valor acumulado")
        self.line, = self.ax.plot([], [], 'b-o')
        plt.ion()
        plt.show()
        
    def agregar_valor(self, valor):
        self.valores.append(valor)
        self.line.set_data(range(1,len(self.valores)+1), self.valores)
        self.ax.relim()
        self.ax.autoscale_view()
        plt.pause(0.05)
        
    def finalizar(self):
        plt.ioff()
        plt.show()

# =============================
# HEURÍSTICAS CONSTRUCTIVAS
# =============================
def mayor_costo(productos, capacidad):
    productos_orden = sorted(productos, key=lambda x: -x['costo'])
    valor, volumen, seleccion = 0, 0, []
    graf = GraficaDinamica("Mayor Costo")
    for p in productos_orden:
        if volumen + p['volumen'] <= capacidad:
            volumen += p['volumen']
            valor += p['costo']
            seleccion.append(p['nombre'])
            graf.agregar_valor(valor)
            time.sleep(0.1)
    graf.finalizar()
    return valor, seleccion

def menor_volumen(productos, capacidad):
    productos_orden = sorted(productos, key=lambda x: x['volumen'])
    valor, volumen, seleccion = 0, 0, []
    graf = GraficaDinamica("Menor Volumen")
    for p in productos_orden:
        if volumen + p['volumen'] <= capacidad:
            volumen += p['volumen']
            valor += p['costo']
            seleccion.append(p['nombre'])
            graf.agregar_valor(valor)
            time.sleep(0.1)
    graf.finalizar()
    return valor, seleccion

def combinacion_lineal(productos, capacidad, repeticiones=1, coeficientes=None):
    if coeficientes is None:
        coeficientes = [(1,1)]*repeticiones
    valor_total, seleccion_total = 0, []
    graf = GraficaDinamica("Mayor Combinación Lineal")
    for i in range(repeticiones):
        k1, k2 = coeficientes[i]
        productos_orden = sorted(productos, key=lambda x: -(k1*x['costo'] + k2*(1/x['volumen'])))
        volumen = 0
        valor_iter = 0
        for p in productos_orden:
            if p['nombre'] not in seleccion_total and volumen + p['volumen'] <= capacidad:
                volumen += p['volumen']
                valor_iter += p['costo']
                seleccion_total.append(p['nombre'])
                graf.agregar_valor(valor_iter)
                time.sleep(0.1)
        valor_total += valor_iter
    graf.finalizar()
    return valor_total, seleccion_total

def costo_volumen(productos, capacidad):
    productos_orden = sorted(productos, key=lambda x: -(x['costo']/x['volumen']))
    valor, volumen, seleccion = 0, 0, []
    graf = GraficaDinamica("Mayor Costo/Volumen")
    for p in productos_orden:
        if volumen + p['volumen'] <= capacidad:
            volumen += p['volumen']
            valor += p['costo']
            seleccion.append(p['nombre'])
            graf.agregar_valor(valor)
            time.sleep(0.1)
    graf.finalizar()
    return valor, seleccion

def azar(productos, capacidad, semilla=None):
    if semilla is not None:
        random.seed(semilla)
    productos_orden = productos.copy()
    random.shuffle(productos_orden)
    valor, volumen, seleccion = 0, 0, []
    graf = GraficaDinamica("Azar")
    for p in productos_orden:
        if volumen + p['volumen'] <= capacidad:
            volumen += p['volumen']
            valor += p['costo']
            seleccion.append(p['nombre'])
            graf.agregar_valor(valor)
            time.sleep(0.1)
    graf.finalizar()
    return valor, seleccion

def alternancia(productos, capacidad, heuristicas):
    valor_total, seleccion_total = 0, []
    graf = GraficaDinamica("Alternancia")
    for h in heuristicas:
        random.shuffle(productos)
        for p in productos:
            if p['nombre'] not in seleccion_total and p['volumen'] <= capacidad:
                valor_total += p['costo']
                capacidad -= p['volumen']
                seleccion_total.append(p['nombre'])
                graf.agregar_valor(valor_total)
                time.sleep(0.1)
    graf.finalizar()
    return valor_total, seleccion_total

def menor_cap_residual(productos, capacidad):
    productos_orden = sorted(productos, key=lambda x: (capacidad - x['volumen']))
    valor, volumen, seleccion = 0, 0, []
    graf = GraficaDinamica("Menor Capacidad Residual")
    for p in productos_orden:
        if volumen + p['volumen'] <= capacidad:
            volumen += p['volumen']
            valor += p['costo']
            seleccion.append(p['nombre'])
            graf.agregar_valor(valor)
            time.sleep(0.1)
    graf.finalizar()
    return valor, seleccion

# =============================
# HEURÍSTICAS DE REDUCCIÓN
# =============================
def red_menor_costo(productos, capacidad):
    productos_orden = sorted(productos, key=lambda x: x['costo'])
    valor, volumen, seleccion = 0,0,[]
    graf = GraficaDinamica("Reducción: Menor Costo")
    for p in productos_orden:
        if volumen + p['volumen'] <= capacidad:
            volumen += p['volumen']
            valor += p['costo']
            seleccion.append(p['nombre'])
            graf.agregar_valor(valor)
            time.sleep(0.1)
    graf.finalizar()
    return valor, seleccion

def red_mayor_volumen(productos, capacidad):
    productos_orden = sorted(productos, key=lambda x: -x['volumen'])
    valor, volumen, seleccion = 0,0,[]
    graf = GraficaDinamica("Reducción: Mayor Volumen")
    for p in productos_orden:
        if volumen + p['volumen'] <= capacidad:
            volumen += p['volumen']
            valor += p['costo']
            seleccion.append(p['nombre'])
            graf.agregar_valor(valor)
            time.sleep(0.1)
    graf.finalizar()
    return valor, seleccion

def menor_combinacion_lineal(productos, capacidad, repeticiones=1, coeficientes=None):
    if coeficientes is None:
        coeficientes = [(1,1)]*repeticiones
    valor_total, seleccion_total = 0, []
    graf = GraficaDinamica("Reducción: Menor Combinación Lineal")
    for i in range(repeticiones):
        k1, k2 = coeficientes[i]
        productos_orden = sorted(productos, key=lambda x: (k1*x['costo'] + k2*(1/x['volumen'])))
        volumen = 0
        valor_iter = 0
        for p in productos_orden:
            if p['nombre'] not in seleccion_total and volumen + p['volumen'] <= capacidad:
                volumen += p['volumen']
                valor_iter += p['costo']
                seleccion_total.append(p['nombre'])
                graf.agregar_valor(valor_iter)
                time.sleep(0.1)
        valor_total += valor_iter
    graf.finalizar()
    return valor_total, seleccion_total

def menor_costo_volumen(productos, capacidad):
    productos_orden = sorted(productos, key=lambda x: x['costo']/x['volumen'])
    valor, volumen, seleccion = 0,0,[]
    graf = GraficaDinamica("Reducción: Menor Costo/Volumen")
    for p in productos_orden:
        if volumen + p['volumen'] <= capacidad:
            volumen += p['volumen']
            valor += p['costo']
            seleccion.append(p['nombre'])
            graf.agregar_valor(valor)
            time.sleep(0.1)
    graf.finalizar()
    return valor, seleccion

def red_azar(productos, capacidad, semilla=None):
    if semilla is not None:
        random.seed(semilla)
    productos_orden = productos.copy()
    random.shuffle(productos_orden)
    valor, volumen, seleccion = 0,0,[]
    graf = GraficaDinamica("Reducción: Azar")
    for p in productos_orden:
        if volumen + p['volumen'] <= capacidad:
            volumen += p['volumen']
            valor += p['costo']
            seleccion.append(p['nombre'])
            graf.agregar_valor(valor)
            time.sleep(0.1)
    graf.finalizar()
    return valor, seleccion

def red_alternancia(productos, capacidad, heuristicas):
    valor_total, seleccion_total = 0, []
    graf = GraficaDinamica("Reducción: Alternancia")
    for h in heuristicas:
        random.shuffle(productos)
        for p in productos:
            if p['nombre'] not in seleccion_total and p['volumen'] <= capacidad:
                valor_total += p['costo']
                capacidad -= p['volumen']
                seleccion_total.append(p['nombre'])
                graf.agregar_valor(valor_total)
                time.sleep(0.1)
    graf.finalizar()
    return valor_total, seleccion_total

# =============================
# HEURÍSTICA DE DESCOMPOSICIÓN
# =============================
def dividir_submochilas(productos, capacidad, num_sub):
    capacidad_sub = capacidad / num_sub
    resultados = []
    for i in range(num_sub):
        print(f"\n--- Submochila {i+1} ---")
        valor, seleccion = mayor_costo(productos, capacidad_sub)
        resultados.append((valor, seleccion))
    return resultados

# =============================
# MENÚ PRINCIPAL
# =============================
def main():
    print("=== METAHEURÍSTICAS POR INDICADORES ===")
    archivo = input("Ingrese archivo de productos: ")
    productos = leer_productos(archivo)
    if not productos:
        return
    capacidad = float(input("Ingrese capacidad de la mochila: "))

    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Heurísticas Constructivas")
        print("2. Heurísticas de Reducción")
        print("3. Heurística de Descomposición")
        print("4. Salir")
        op = input("Seleccione una opción: ")

        if op=="1":
            print("\nOpciones: 1-MC 2-MV 3-MCL 4-CV 5-A 6-ALT 7-MCR")
            sel = input("Seleccione heurísticas (comas): ").split(",")
            for s in sel:
                if s.strip()=="1": mayor_costo(productos, capacidad)
                elif s.strip()=="2": menor_volumen(productos, capacidad)
                elif s.strip()=="3":
                    rep = int(input("Repeticiones: "))
                    coefs = []
                    for i in range(rep):
                        k1 = float(input(f"k1 rep {i+1}: "))
                        k2 = float(input(f"k2 rep {i+1}: "))
                        coefs.append((k1,k2))
                    combinacion_lineal(productos, capacidad, rep, coefs)
                elif s.strip()=="4": costo_volumen(productos, capacidad)
                elif s.strip()=="5": 
                    sem = int(input("Semilla: "))
                    azar(productos, capacidad, sem)
                elif s.strip()=="6": 
                    alternancia(productos, capacidad, [productos, productos])
                elif s.strip()=="7": menor_cap_residual(productos, capacidad)
        elif op=="2":
            print("\nOpciones: 1-MC 2-MV 3-MCL 4-CV 5-A 6-ALT")
            sel = input("Seleccione heurísticas (comas): ").split(",")
            for s in sel:
                if s.strip()=="1": red_menor_costo(productos, capacidad)
                elif s.strip()=="2": red_mayor_volumen(productos, capacidad)
                elif s.strip()=="3":
                    rep = int(input("Repeticiones: "))
                    coefs = []
                    for i in range(rep):
                        k1 = float(input(f"k1 rep {i+1}: "))
                        k2 = float(input(f"k2 rep {i+1}: "))
                        coefs.append((k1,k2))
                    menor_combinacion_lineal(productos, capacidad, rep, coefs)
                elif s.strip()=="4": menor_costo_volumen(productos, capacidad)
                elif s.strip()=="5": 
                    sem = int(input("Semilla: "))
                    red_azar(productos, capacidad, sem)
                elif s.strip()=="6": 
                    red_alternancia(productos, capacidad, [productos, productos])
        elif op=="3":
            num_sub = int(input("Número de submochilas: "))
            dividir_submochilas(productos, capacidad, num_sub)
        elif op=="4":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__=="__main__":
    main()
