from ciudad import Ciudad
from data import ciudades, distancias_entre_ciudades

"""Forma lista ciudades:
    [Ciudad(1,"Buenos Aires"),
    Ciudad(2, "Cordoba"),
    ...
    ]
"""


"""Forma lista distancias:
    [
    (Ciudad(1,"Buenos Aires"), Ciudad(2, "Cordoba"),646 ),
    (Ciudad(1,"Buenos Aires"), Ciudad(3, "Corrientes"),792 ),
    ...
    ]
"""




def get_distancia(ciu1:Ciudad,ciu2:Ciudad):
    """Funcion que dadas 2 ciudades retorna la distancia entre ellas
    """
    if not isinstance(ciu1, Ciudad) or not isinstance(ciu2, Ciudad):
        raise ValueError("Se deben ingresar instancias de provincias")
    if ciu1 == ciu2:
        return 0
    distancias = distancias_entre_ciudades

    for dist in distancias:
        if ciu1 in dist and ciu2 in dist:
            return dist[2]

    else:
        return None
