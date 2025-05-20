from enum import Enum
from collections import namedtuple

BoundingBox = namedtuple("BoundingBox", ["top", "bottom", "left", "right"])

class BoundingBoxEnum (Enum):
    PORTO = BoundingBox(41.2100, 41.1150, -8.5400, -8.6890)
    LISBON = BoundingBox(38.8070, 38.6914, -9.0921, -9.2308)
    