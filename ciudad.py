from dataclasses import dataclass
from typing import ClassVar, Tuple, List


@dataclass
class Ciudad:

    _id:int
    _nombre:str
    _ubicacion:List[int]

    def __init__(self,id:int , nombre:str, ubicacion:List[int]):
        self._id =  id
        self._nombre = nombre
        self._ubicacion = ubicacion


    @property
    def id(self)-> int:
        return self._id

    @property
    def ubicacion(self) -> List[int]:
        return self._ubicacion

    @property
    def nombre(self) -> str:
        return self._nombre







    def __str__(self):
        return self.nombre


    def __repr__(self):
        return str(self.id)

    def __eq__(self,other) -> bool:
        if not isinstance(other, Ciudad):
            return False
        return self.id == other.id

    def __hash__(self):
        return self.id





