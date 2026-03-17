from dataclasses import dataclass



@dataclass
class Entity:
    name: str
    state: str
    health: float

@dataclass
class Player(Entity):
    '''Single use componenet for identifying the player'''

@dataclass
class Position:
    Chunk: list
    xOffset: float
    yOffset: float

@dataclass
class Velocity:
    xVel: float = 0.0
    yvel: float = 0.0

@dataclass
class Renderable:
    image: str
    imageCoords: tuple

@dataclass
class Animated(Renderable):
    #dictioanry of coords based on the state
    frames: dict
    frame: int