from pathlib import Path

import typer

from routing_optimization.algorithm import plan_route
from routing_optimization.utils import load_input

app = typer.Typer()


def plan_route_from_file(path: Path) -> dict:
    """
    Main function to plan the route based on input data from a JSON file.
    Args:
        path (Path): Path to the JSON input file.
    Returns:
        dict: A dictionary containing the planned route details.
    """

    deliveries, pickups, vehicle, depot = load_input(path)
    route_info = plan_route(deliveries, pickups, vehicle, depot)

    return route_info


@app.command()
def main(path: Path) -> None:
    """
    CLI entry to plan the route based on input data from a JSON file.
    Args:
        path (Path): Path to the JSON input file.
    Returns:
        dict: A dictionary containing the planned route details.
    """

    deliveries, pickups, vehicle, depot = load_input(path)
    route_info = plan_route(deliveries, pickups, vehicle, depot)

    typer.echo(f"Total Distance: {route_info['total_distance']:.2f}\n")
    typer.echo("Route IDs:")
    typer.echo(" -> ".join(route_info["route_ids"]))


if __name__ == "__main__":
    app()
