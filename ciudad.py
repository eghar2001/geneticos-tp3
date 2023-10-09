from dataclasses import dataclass
from typing import ClassVar, Tuple, List


@dataclass
class Ciudad:

    _id:int
    _nombre:str

    def __init__(self,id:int , nombre:str):
        self._id =  id
        self._nombre = nombre


    @property
    def id(self)-> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self,value:str):
        self._nombre = value





    def __str__(self):
        return self._nombre


    def __repr__(self):
        return ""+self._nombre

    def __eq__(self,other) -> bool:
        if not isinstance(other, Ciudad):
            return False
        return self.id == other.id

    def __hash__(self):
        return self.id





