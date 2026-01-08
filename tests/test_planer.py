from routing_optimization.algorithm import (
    is_route_feasible,
    select_deliveries,
    select_pickup,
)
from routing_optimization.models import Delivery, Depot, Pickup, Vehicle


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


def test_feasible_route():
    vehicle = Vehicle(capacity=5)
    depot = Depot()
    d1 = Delivery(id=0, x=0, y=0, capacity=2)
    d2 = Delivery(id=1, x=1, y=1, capacity=1)
    p1 = Pickup(id=2, x=2, y=2, capacity=2)

    route = [depot, d1, d2, p1, depot]

    assert is_route_feasible(route, vehicle) is True


def test_infeasible_route():
    vehicle = Vehicle(capacity=4)
    depot = Depot()
    d1 = Delivery(id=0, x=0, y=0, capacity=2)
    d2 = Delivery(id=1, x=1, y=1, capacity=1)
    p1 = Pickup(id=2, x=2, y=2, capacity=5)

    route = [depot, d1, d2, p1, depot]

    assert is_route_feasible(route, vehicle) is False
