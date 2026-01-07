from routing_optimization.utils import distance
from routing_optimization.models import Event

def test_distance():
    event_a = Event(id=0, x=0.0, y=0.0, capacity=10.0)
    event_b = Event(id=1, x=3.0, y=4.0, capacity=15.0)
    dist = distance(event_a, event_b)
    assert dist == 5.0