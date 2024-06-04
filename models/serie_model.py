
from dataclasses import dataclass
from typing import Any

from models.season_model import SeasonModel


@dataclass
class SerieModel:
    id:int
    name:str
    portada:str
    poster:str
    description:str
    populate:float
    trailer:str
    temporadas:list[SeasonModel]
