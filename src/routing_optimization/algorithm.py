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
    if not combined_rank:
        raise ValueError("No feasible pickups available within vehicle capacity.")
    best_pickup_id = min(combined_rank, key=combined_rank.get)
    best_pickup = next(p for p in feasible_pickups if p.id == best_pickup_id)
    return best_pickup

def nearest_neighbor_route(deliveries: List[Delivery], pickup: Pickup, vehicle: Vehicle, depot: Depot) -> List:
    """
    Constructs a route using the Nearest Neighbor heuristic with vehicle capacity constraints.

    Args:
        deliveries (List[Delivery]): A list of selected delivery events.
        pickup (Pickup): The selected pickup event.
        vehicle (Vehicle): The vehicle assigned to the route.
        depot (Depot): The starting and ending point for the vehicle.
    Returns:
        List: A list representing the sequence of stops in the route.
    """
    unvisited_deliveries = deliveries.copy()
    pickup_unvisited = True

    current_load = sum(d.capacity for d in deliveries)
    route = [depot]
    current = depot

    while unvisited_deliveries or pickup_unvisited:
        candidates = unvisited_deliveries.copy()
        if pickup_unvisited and current_load + pickup.capacity <= vehicle.capacity:
            candidates.append(pickup)

        next_event = min(candidates, key=lambda e: distance(current, e))
        route.append(next_event)
        current = next_event

        if isinstance(next_event, Delivery):
            current_load -= next_event.capacity
            unvisited_deliveries.remove(next_event)
        else:
            current_load += next_event.capacity
            pickup_unvisited = False

    route.append(depot)
    return route

def is_route_feasible(route: List, vehicle: Vehicle) -> bool:
    """
    Capacity feasibility check for a route during 2-opt optimization.
    """

    load = sum(e.capacity for e in route if isinstance(e, Delivery))

    for e in route:
        if isinstance(e, Delivery):
            load -= e.capacity
        elif isinstance(e, Pickup):
            # ONLY possible violation point
            return load + e.capacity <= vehicle.capacity

    return True

def two_opt(route: List, vehicle: Vehicle) -> List:
    """
    Applies the 2-opt optimization algorithm to improve the given route.

    Args:
        route (List): The initial route to be optimized.
        vehicle (Vehicle): The vehicle assigned to the route.
    Returns:
        List: The optimized route after applying 2-opt.
    """
    improved = True
    best_route = route.copy()
    best_distance = route_distance(route)
    n = len(best_route) - 1

    while improved:
        improved = False
        # i, j are the indices of the route to be reversed starting from 0
        for i in range(n - 2):
            for j in range(i + 2, n):
                new_route = best_route[:i+1] + best_route[i+1:j+1][::-1] + best_route[j+1:]
                if is_route_feasible(new_route, vehicle):
                    new_distance = route_distance(new_route)
                    if new_distance < best_distance:
                        best_route = new_route
                        best_distance = new_distance
                        improved = True

    return best_route

def three_opt(route: List, vehicle: Vehicle) -> List:
    """
    Applies the 3-opt optimization algorithm to improve the given route.

    Args:
        route (List): The initial route to be optimized.
        vehicle (Vehicle): The vehicle assigned to the route.
    Returns:
        List: The optimized route after applying 3-opt.
    """
    improved = True
    best_route = route.copy()
    best_distance = route_distance(route)
    n = len(best_route) - 1

    while improved:
        improved = False
        # Iterate through all triplets of edges (i, j, k)
        for i in range(n - 4):
            for j in range(i + 2, n - 2):
                for k in range(j + 2, n):
                    # Generate all 7 possible 3-opt reconnections
                    segment1 = best_route[:i+1]
                    segment2 = best_route[i+1:j+1]
                    segment3 = best_route[j+1:k+1]
                    segment4 = best_route[k+1:]
                    segments = [
                        segment1 + segment2[::-1] + segment3 + segment4,  # Case 1
                        segment1 + segment2 + segment3[::-1] + segment4,  # Case 2
                        segment1 + segment2[::-1] + segment3[::-1] + segment4,  # Case 3
                        segment1 + segment3 + segment2 + segment4,  # Case 4
                        segment1 + segment3[::-1] + segment2 + segment4,  # Case 5
                        segment1 + segment3 + segment2[::-1] + segment4,  # Case 6
                        segment1 + segment3[::-1] + segment2[::-1] + segment4,  # Case 7
                    ]
                    
                    for new_route in segments:
                        if is_route_feasible(new_route, vehicle):
                            new_distance = route_distance(new_route)
                            if new_distance < best_distance:
                                best_route = new_route
                                best_distance = new_distance
                                improved = True

    return best_route



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
    
    # Step 3: Build a route using the Nearest Neighbor heuristic
    nn_route = nearest_neighbor_route(selected_deliveries, selected_pickup, vehicle, depot)
    
    # Step 4: 2-opt/3-opt optimization to improve the route
    if len(nn_route) >= 4: # Minimum length for 2-opt
        route_opt = two_opt(nn_route, vehicle)
        if len(route_opt) >= 6: # Minimum length for 3-opt
            route_opt = three_opt(route_opt, vehicle)
    else:
        route_opt = nn_route

    # Step 5: Return the route details
    result = {"total_distance": route_distance(route_opt),
              "route_ids": get_route_ids(route_opt),
              "route": route_opt}
    return result