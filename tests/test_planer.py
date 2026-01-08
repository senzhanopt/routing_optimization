from routing_optimization.models import Delivery, Pickup, Vehicle, Depot
from routing_optimization.algorithm import select_deliveries, select_pickup

def test_select_deliveries():
    deliveries = [
        Delivery(id=0, x=0, y=0, capacity=3),
        Delivery(id=1, x=1, y=1, capacity=1),
        Delivery(id=2, x=2, y=2, capacity=5),
    ]
    vehicle = Vehicle(capacity=4)

    selected = select_deliveries(deliveries, vehicle)

    assert len(selected) == 2
    assert sum(d.capacity for d in selected) == 4

def test_select_pickup():
    depot = Depot()
    vehicle = Vehicle(capacity=5)

    pickups = [
        Pickup(id=0, x=10, y=0, capacity=4),
        Pickup(id=1, x=1, y=1, capacity=2),
        Pickup(id=2, x=1, y=2, capacity=4),
    ]

    pickup = select_pickup(pickups, depot, vehicle)

    assert pickup.id == 1
    assert pickup.capacity == 2