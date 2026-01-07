import math
from routing_optimization.models import Event

def distance(a: Event, b: Event) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)