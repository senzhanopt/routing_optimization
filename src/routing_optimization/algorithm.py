from routing_optimization.models import Delivery, Pickup, Vehicle, Depot
from routing_optimization.utils import distance, route_distance, get_route_ids
from typing import List

def select_deliveries(deliveries: List[Delivery], vehicle: Vehicle) -> List[Delivery]:
    """
    Sorts and selects deliveries based on vehicle capacity using a greedy approach.

    Args:
        deliveries (List[Delivery]): A list of delivery events to be completed.
        vehicle (Vehicle): The vehicle assigned to the route.
    Returns:
        List[Delivery]: A list of selected deliveries that fit within the vehicle's capacity.
    """
    sorted_deliveries = sorted(deliveries, key=lambda d: d.capacity)
    selected_deliveries: List[Delivery] = []
    current_load = 0.0
    for d in sorted_deliveries:
        if current_load + d.capacity <= vehicle.capacity:
            selected_deliveries.append(d)
            current_load += d.capacity
        else:
            break
    return selected_deliveries

def select_pickup(pickups: List[Pickup], depot: Depot, vehicle: Vehicle) -> Pickup:
    """
    Selects the best pickup based on distance from depot and capacity.

    Args:
        pickups (List[Pickup]): A list of pickup events with only one to be completed.
        depot (Depot): The starting and ending point for the vehicle.
    Returns:
        Pickup: The selected pickup event.
    """

    # Filter pickups that fit within vehicle capacity
    feasible_pickups = [p for p in pickups if p.capacity <= vehicle.capacity]
    # Sort by distance from depot and capacity
    distance_sorted = sorted(feasible_pickups, key=lambda p: distance(depot, p))
    capacity_sorted = sorted(feasible_pickups, key=lambda p: p.capacity)
    # Combine rankings
    distance_rank = {p.id: rank for rank, p in enumerate(distance_sorted)}
    capacity_rank = {p.id: rank for rank, p in enumerate(capacity_sorted)}
    combined_rank = {p.id: distance_rank[p.id] + capacity_rank[p.id] for p in feasible_pickups}
    # Select pickup with the best combined rank
    best_pickup_id = min(combined_rank, key=combined_rank.get)
    best_pickup = next(p for p in feasible_pickups if p.id == best_pickup_id)
    return best_pickup

def plan_route(deliveries: List[Delivery], pickups: List[Pickup], vehicle: Vehicle, depot: Depot = Depot()) -> dict:
    """
    Plans an optimized route for a vehicle to handle deliveries and pickups starting and ending at the depot.

    Args:
        deliveries (List[Delivery]): A list of delivery events to be completed.
        pickups (List[Pickup]): A list of pickup events with only one to be completed.
        vehicle (Vehicle): The vehicle assigned to the route.
        depot (Depot, optional): The starting and ending point for the vehicle. Defaults to Depot(0.0, 0.0).
    Returns:
        dict: A dictionary containing the optimized route details including total distance and sequence of stops.
    """

    # Step 1: Sort deliveries based on capacity in ascending order and greedily add deliveries
    selected_deliveries = select_deliveries(deliveries, vehicle)
    
    # Step 2: Select the pickup by ranking both distance from depot and capacity
    selected_pickup = select_pickup(pickups, depot, vehicle)
    
    # Step 3: Construct the route starting and ending at the depot
    route_base = [depot] + selected_deliveries + [selected_pickup] + [depot]
    route_distance_base = route_distance(route_base)

    # Step 4: Return the route details
    result = {"total_distance": route_distance_base,
              "route_ids": get_route_ids(route_base)}
    return result