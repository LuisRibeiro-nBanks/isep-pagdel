from enum import Enum
from collections import namedtuple

Locatión = namedtuple("BoundingBox", ["top", "bottom", "left", "right", "code"])

class LocationEnum (Enum):
    PORTO = Locatión(41.2100, 41.1150, -8.5400, -8.6890, "PRT_porto")
    LISBON = Locatión(38.8070, 38.6914, -9.0921, -9.2308, "PRT_lisbon")    