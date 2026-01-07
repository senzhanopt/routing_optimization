from routing_optimization.main import main
from routing_optimization.utils import visualize_route
from pathlib import Path

data_file = Path(__file__).resolve().parent.parent / "data" / "case2.json"
result = main(data_file)

print(result)
visualize_route(result["route"])
