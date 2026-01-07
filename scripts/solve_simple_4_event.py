from routing_optimization.main import main
from pathlib import Path

data_file = Path(__file__).resolve().parent.parent / "data" / "simple_4_events.json"
result = main(data_file)

print(result)