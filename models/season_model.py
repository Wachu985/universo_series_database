from dataclasses import dataclass

@dataclass
class SeasonModel:
    name:str
    url:str
    caps: list[str]
    subtitle: list[str]