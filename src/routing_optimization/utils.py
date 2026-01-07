import math
import json
from typing import List, Tuple
from pathlib import Path
from routing_optimization.models import Event, Delivery, Pickup, Depot, Vehicle

def distance(a: Event, b: Event) -> float:
    """
    Calculates the Euclidean distance between two events.
    Args:
        a (Event): The first event.
        b (Event): The second event.
    Returns:
        float: The Euclidean distance between the two events.
    """
    return math.hypot(a.x - b.x, a.y - b.y)

def route_distance(route: list[Event]) -> float:
    """
    Calculates the total distance of a given route.
    Args:
        route (list[Event]): A list of events representing the route.
    Returns:
        float: The total distance of the route.
    """
    if len(route) < 2:
        return 0.0
    total_distance = 0.0
    for i in range(len(route) - 1):
        total_distance += distance(route[i], route[i + 1])
    return total_distance

def get_route_ids(route: list[Event]) -> list[str]:
    """
    Extracts the IDs of events in the given route.
    Args:
        route (list[Event]): A list of events representing the route.
    Returns:
        list[str]: A list of event IDs in the route.
    """
    route_ids = []

    for e in route:
        if isinstance(e, Delivery):
            route_ids.append(f"D{e.id}")
        elif isinstance(e, Pickup):
            route_ids.append(f"P{e.id}")
        else:  # Depot
            route_ids.append("Depot")
    return route_ids

def load_input(path: Path) -> Tuple[List[Delivery], List[Pickup], Vehicle, Depot]:
    """
    Loads JSON input from a file (Path) and converts it into Pydantic models.

    Args:
        path (Path): Path to the JSON input file.

    Returns:
        Tuple[List[Delivery], List[Pickup], Vehicle, Depot]: Pydantic objects ready for plan_route.
    """
    data = json.loads(path.read_text())

    vehicle = Vehicle(capacity=data["vehicle_capacity"])
    deliveries = [Delivery(**d) for d in data.get("deliveries", [])]
    pickups = [Pickup(**p) for p in data.get("pickups", [])]
    depot_data = data.get("depot", {})
    depot = Depot(x=depot_data.get("x", 0.0), y=depot_data.get("y", 0.0))

    return deliveries, pickups, vehicle, depot