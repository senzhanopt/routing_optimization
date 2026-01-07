from routing_optimization.algorithm import plan_route
from pathlib import Path
from routing_optimization.utils import load_input

def main(path: Path) -> dict:
    """
    Main function to plan the route based on input data from a JSON file.
    Args:
        path (Path): Path to the JSON input file.
    Returns:
        dict: A dictionary containing the planned route details.
    """
    # Load data from the given path (implementation not shown)
    deliveries, pickups, vehicle, depot = load_input(path)

    # Plan the route
    route_info = plan_route(deliveries, pickups, vehicle, depot)

    return route_info
