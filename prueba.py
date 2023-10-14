from copy import deepcopy
from typing import List

from ciudad import Ciudad
from data import ciudades
from utils import get_distancia, dibujar_recorrido
import random
import os

def get_recorrido_minimo( ciu_inicial:Ciudad):
    """Funcion que obtiene el recorrido minimo
    para visitar todas las capitales del pais
    Retorna una tupla que contiene la lista del recorrido, y la distancia total recorrida"""
    ciudades_no_recorridas = deepcopy(ciudades)
    ciudades_no_recorridas.remove(ciu_inicial)
    recorrido = [ciu_inicial]
    ciu_actual = ciu_inicial
    distancia_recorrida = 0
    for i in range(len(ciudades)-1):
       min_ciu = ciudades_no_recorridas[0]
       min_dist = get_distancia(min_ciu, ciu_actual)
       for ciu in ciudades_no_recorridas:
           distancia = get_distancia(ciu_actual, ciu)
           if distancia < min_dist:
               min_dist = distancia
               min_ciu = ciu
       ciudades_no_recorridas.remove(min_ciu)
       recorrido.append(min_ciu)
       ciu_actual = min_ciu
       distancia_recorrida += min_dist
    recorrido.append(ciu_inicial)
    distancia_recorrida += get_distancia(ciu_actual, ciu_inicial)
    return recorrido,distancia_recorrida







def opcion1():
    mejorRecorrido = []

    for (i, prov) in enumerate(ciudades):
        print(f"{i}--{prov}")
    print("Ingrese numero de la provinica que quiera elegir:")
    ciu_inicial_index = int(input())
    ciu_inicial = ciudades[ciu_inicial_index]
    recorrido,distancia_recorrida = get_recorrido_minimo(ciu_inicial)
    print(f"Ciudad inicial: {ciu_inicial}")
    print(f"Longitud de trayecto: {distancia_recorrida}")
    print(f"Trayecto: \n{recorrido}")
    dibujar_recorrido(recorrido,distancia_recorrida)


def opcion2():
    recorridos = [get_recorrido_minimo(ciu) for ciu in ciudades ]
    (min_recorrido, min_distancia) = (recorridos[0][0],recorridos[0][1])
    for (reco, dist) in recorridos:
        if dist<min_distancia:
            min_recorrido = reco
            min_distancia = dist
    print(f"Ciudad inicial: {min_recorrido[0]}")
    print(f"Longitud de trayecto: {min_distancia}")
    print(f"Trayecto: \n{min_recorrido}")
    dibujar_recorrido(min_recorrido,min_distancia)


def opcion3():
    def func_obj(cromosoma:List[Ciudad]):
        distancia = 0
        ciudad_anterior = cromosoma[0]
        for ciudad in cromosoma:
            distancia += get_distancia(ciudad, ciudad_anterior)
            ciudad_anterior = ciudad
        return distancia

    def seleccion_torneo(poblacion, poblacion_fitness):
        seleccionados = []
        for i in range(2):
            # torneo = random.sample(poblacion, 2) # selecciona 2 individuos al azar de la población
            """
            aptitudes = [individuo.aptitud() for individuo in torneo] # evalúa la aptitud de cada uno
            """
            torneo = [random.randint(0, len(poblacion) - 1), random.randint(0, len(poblacion) - 1)]
            min_poblacion_fitness = min([poblacion_fitness[i] for i in torneo])
            index_min_fitness = poblacion_fitness.index(min_poblacion_fitness)
            seleccionados.append(poblacion[index_min_fitness])
        return tuple(seleccionados)
    def crossover(padre1:List[Ciudad],padre2:List[Ciudad]):
        hijo1 = []
        hijo2 = []
        for i in range(len(padre1)):
            hijo1.append(0)
            hijo2.append(0)
        indice = 0

        elemento_inicial = padre1[0]
        while padre2[indice] != elemento_inicial:
            hijo1[indice] = padre1[indice]
            indice = padre1.index(padre2[indice])
        hijo1[indice] = padre1[indice]

        for (i,ciu) in enumerate(hijo1):
            if ciu == 0:
                hijo1[i] = padre2[i]
                hijo2[i] = padre1[i]
            else:
                hijo2[i] = padre2[i]

        return hijo1, hijo2




    poblacion_inicial = []
    for i in range(50):
        cromosoma = random.sample(ciudades, len(ciudades))
        poblacion_inicial.append(cromosoma)

    poblacion_anterior = poblacion_inicial
    poblacion_nueva = []
    for i in range(len(poblacion_inicial)//2):

        funciones_objetivo = [func_obj(cromo) for cromo in poblacion_anterior]

        total_funciones_obj = sum(funciones_objetivo)

        poblacion_fitness = [fun/total_funciones_obj for fun in funciones_objetivo]
        seleccionados  = seleccion_torneo(poblacion_anterior, poblacion_fitness)
        (hijo1, hijo2) = crossover(seleccionados[0],seleccionados[1])
        poblacion_nueva.append(hijo1)
        poblacion_nueva.append(hijo2)











##MENU
def menu(opciones):
    while (opciones < 4):
        os.system('cls')
        print("Selecciona una opcion")
        print()
        print("1- Busqueda heuristica ingresando una capital")
        print("2- Busqueda heuristica con minimo posible")
        print("3- Menor recorrido posible utilizando algoritmos geneticos")
        print("0- Salir")
        opciones = int(input("Ingrese una opcion: "))
        if opciones == 1:
            opcion1()

        if opciones == 2:
            opcion2()

        if opciones == 3:
            opcion3()

        if opciones == 0:
            break



opciones = 1
menu(opciones)
input()