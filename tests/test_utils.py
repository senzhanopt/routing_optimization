from routing_optimization.utils import distance, route_distance, get_route_ids
from routing_optimization.models import Event, Depot, Delivery, Pickup

def test_distance():
    event_a = Event(id=0, x=0.0, y=0.0, capacity=10.0)
    event_b = Event(id=1, x=3.0, y=4.0, capacity=15.0)
    dist = distance(event_a, event_b)
    assert dist == 5.0

def test_route_distance():
    depot = Depot(x=0.0, y=0.0)
    d0 = Delivery(id=0, x=3.0, y=4.0, capacity=1.0)
    d1 = Delivery(id=1, x=6.0, y=8.0, capacity=1.0)

    route = [depot, d0, d1, depot]

    assert route_distance(route) == 20.0

def test_get_route_ids():
    depot = Depot()
    d = Delivery(id=0, x=1.0, y=1.0, capacity=1.0)
    p = Pickup(id=0, x=2.0, y=2.0, capacity=1.0)

    route = [depot, d, p, depot]

    assert get_route_ids(route) == ["Depot", "D0", "P0", "Depot"]