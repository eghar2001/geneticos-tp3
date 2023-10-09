from copy import deepcopy

import openpyxl
from ciudad import Ciudad



excel_dataframe = openpyxl.load_workbook("TablaCapitales.xlsx")

dataframe = excel_dataframe.active


def get_ciudades():
    """Funcion que retorna una lista con todas las ciudades disponibles"""
    Ciudad._last_id = 0
    cant_columnas = dataframe.max_column - 2
    ciudades = []
    id = 0
    for col in dataframe.iter_cols(2,cant_columnas):
        id+=1
        ciudades.append(Ciudad(id, col[0].value))
    return ciudades



def get_distancias():
    """Funcion que retorna un conjunto de distancias entre distintas ciudades
        Retorna un set conformado por tuplas (ciu_1, ciu_2, dist)
    """
    cant_filas = dataframe.max_row - 2
    cant_columnas = dataframe.max_column - 2
    distancias = []
    ciudades = get_ciudades()
    fila_inicial = 3
    for ind_col in range(2,cant_columnas ):
        ciu_act = ciudades[ind_col-2]
        for ind_row in range(fila_inicial,cant_filas+1):
            ciu_dist = ciudades[ind_row-2]
            dist = int(dataframe.cell(column=ind_col, row=ind_row).value)
            distancias.append((ciu_act, ciu_dist, dist))
        fila_inicial += 1
    return distancias

ciudades = get_ciudades()
distancias_entre_ciudades = get_distancias()