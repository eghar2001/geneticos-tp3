from copy import deepcopy
from typing import List
from functools import reduce
from ciudad import Ciudad
import matplotlib.pyplot as plt
from data import ciudades, distancias_entre_ciudades
from utils import  dibujar_recorrido
import random
import os


CANTIDAD_ITERACIONES = 200
PROBABILIDAD_CROSSOVER = 0.75
PROBABILIDAD_MUTACION = 0.01
CANTIDAD_ELITISMO = 10

distancias = distancias_entre_ciudades


def get_ciudad(ciudad_id:int):
    for ciu in ciudades:
        if ciu.id == ciudad_id:
            return ciu
    return None


def get_distancia(ciu1_id:int,ciu2_id:Ciudad):
    """Funcion que dadas 2 ciudades retorna la distancia entre ellas
    """

    for dist in distancias:
        if (ciu1_id== dist[0] or ciu1_id == dist[1]) and (ciu2_id == dist[0] or ciu2_id == dist[1]):
            return dist[2]

    else:
        return None
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
       min_dist = get_distancia(min_ciu.id, ciu_actual.id)
       for ciu in ciudades_no_recorridas:
           distancia = get_distancia(ciu_actual.id, ciu.id)
           if distancia < min_dist:
               min_dist = distancia
               min_ciu = ciu
       ciudades_no_recorridas.remove(min_ciu)
       recorrido.append(min_ciu)
       ciu_actual = min_ciu
       distancia_recorrida += min_dist
    recorrido.append(ciu_inicial)
    distancia_recorrida += get_distancia(ciu_actual.id, ciu_inicial.id)
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


    def elitismo(poblacion, poblacion_fitness):
        poblacion_ordenada = sorted(zip(poblacion_fitness,poblacion), reverse= True)
        ciudades_por_elitismo = []
        for i in range(CANTIDAD_ELITISMO):
            ciudades_por_elitismo.append(poblacion_ordenada[i][1])
        return ciudades_por_elitismo

    def seleccion_torneo(poblacion, poblacion_fitness):
        seleccionados = []
        for i in range(2):
            # torneo = random.sample(poblacion, 2) # selecciona 2 individuos al azar de la población
            """
            aptitudes = [individuo.aptitud() for individuo in torneo] # evalúa la aptitud de cada uno
            """
            torneo = [random.randint(0, len(poblacion) - 1), random.randint(0, len(poblacion) - 1)]
            min_poblacion_fitness = max([poblacion_fitness[i] for i in torneo])
            index_max_fitness = poblacion_fitness.index(min_poblacion_fitness)
            seleccionados.append(poblacion[index_max_fitness])
        return tuple(seleccionados)

    def crossover(padre1:List[Ciudad],padre2:List[Ciudad]):
        if random.random() < PROBABILIDAD_CROSSOVER:
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
        else:
            return padre1, padre2

    def mutacion(cromosoma):
        if random.random() < PROBABILIDAD_MUTACION:
            ind1 = random.randint(0,len(cromosoma)-1)
            ind2 = random.randint(0,len(cromosoma)-1)
            while ind1 == ind2:
                ind2 = random.randint(0, len(cromosoma)-1)
            aux = cromosoma[ind1]
            cromosoma[ind1] = cromosoma[ind2]
            cromosoma[ind2]=aux




    historico_minimo=[]
    historico_maximo = []
    historico_promedio = []

    ciudades_id = [ciudad.id for ciudad in ciudades]
    #Generamos Poblacion Inicial
    poblacion_inicial = []
    for i in range(50):
        cromosoma = random.sample(ciudades_id, len(ciudades_id))
        poblacion_inicial.append(cromosoma)

    poblacion_anterior = poblacion_inicial

    for i in range(CANTIDAD_ITERACIONES):

        funciones_objetivo = [func_obj(cromo) for cromo in poblacion_anterior]
        poblacion_fitness = [1 / fun for fun in funciones_objetivo]
        poblacion_nueva = elitismo(poblacion_anterior, poblacion_fitness)
        minimo_pob = min(funciones_objetivo)
        maximo_pob = max(funciones_objetivo)
        promedio_pob = sum(funciones_objetivo)/ len(funciones_objetivo)

        historico_minimo.append(minimo_pob)
        historico_maximo.append(maximo_pob)
        historico_promedio.append(promedio_pob)

        print(f"ITERACION {i}")
        print(f"maximo: {maximo_pob}")
        print(f"minimo: {minimo_pob}")
        print(f"promedio: {promedio_pob}")
        for j in range((len(poblacion_inicial)-CANTIDAD_ELITISMO)//2):
            seleccionados  = seleccion_torneo(poblacion_anterior, poblacion_fitness)
            (hijo1, hijo2) = crossover(seleccionados[0],seleccionados[1])
            mutacion(hijo1)
            mutacion(hijo2)
            poblacion_nueva.append(hijo1)
            poblacion_nueva.append(hijo2)

        poblacion_anterior = poblacion_nueva
    funciones_objetivo = [func_obj(reco) for reco in poblacion_anterior]
    minimo_pob = min(zip(funciones_objetivo, poblacion_anterior))
    maximo_pob = max(funciones_objetivo)
    promedio_pob = sum(funciones_objetivo) / len(funciones_objetivo)
    historico_minimo.append(minimo_pob[0])
    historico_maximo.append(maximo_pob)
    historico_promedio.append(promedio_pob)
    print(f"ITERACION 200")
    print(f"maximo: {maximo_pob}")
    print(f"minimo: {minimo_pob[0]}")
    print(f"promedio: {promedio_pob}")
    recorrido = [get_ciudad(id) for id in minimo_pob[1]]
    poblaciones = [i for i in range(len(historico_promedio))]
    plt.plot(poblaciones, historico_maximo, "g", label="max")
    plt.plot(poblaciones, historico_minimo, "b", label="avg")
    plt.plot(poblaciones, historico_promedio, "r", label="min")
    plt.title("Máximo, mínimo y promedio Historico")
    plt.xlabel("Numero de iteraciones")
    plt.ylabel("Valores")
    plt.show()
    dibujar_recorrido(recorrido, minimo_pob[0])












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