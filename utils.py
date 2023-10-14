from copy import deepcopy
from typing import List

from ciudad import Ciudad
from data import ciudades, distancias_entre_ciudades
import folium
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
        raise ValueError("Se deben ingresar instancias de Ciudades")
    if ciu1 == ciu2:
        return 0
    distancias = distancias_entre_ciudades

    for dist in distancias:
        if ciu1 in dist and ciu2 in dist:
            return dist[2]

    else:
        return None


def dibujar_recorrido(recorrido:List[Ciudad], distancia:int):

    mapObj = folium.Map(location = [-39.2198564,-65.6193271], zoom_start=4)

    icono_inicio = folium.Icon(icon = "star",prefix = "fa", color="red" )
    ciu_inicial = recorrido[0]

    folium.Marker(location=ciu_inicial.ubicacion, tooltip= f"0: {ciu_inicial.nombre}", icon=icono_inicio).add_to(mapObj)


    ciu_anterior = ciu_inicial
    for (i,ciu) in enumerate(recorrido):
        if ciu != ciu_anterior:
            folium.PolyLine([ciu_anterior.ubicacion,ciu.ubicacion], color="gray", weight = 2).add_to(mapObj)
            ciu_anterior = ciu
        if ciu != ciu_inicial:
            folium.Marker(location = ciu.ubicacion,tooltip=f"{i}: {ciu.nombre}").add_to(mapObj)
    mapObj.get_root().html.add_child(folium.Element("""
        <style>
            .mapText{
                display:inline;
                position:absolute;
                top:0;
                right:0;
                padding:15px;
                z-index:30000;
                background-color: black;
                color:white;
            }
        </style>"""))
    mapObj.get_root().html.add_child(folium.Element(f"""    
    <h3 class="mapText">Distancia recorrida: {distancia}</h3>
    """))

    mapObj.show_in_browser()
