import json
from typing import Any
from pathlib import Path
import datetime

class ReportGenerator:
    @staticmethod
    def save_report(data: Any, target: str, output_path: str, format: str = "json"):
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            report = {
                "target": target,
                "date": datetime.datetime.now().isoformat(),
                "data": data
            }
            with open(path, 'w') as f:
                json.dump(report, f, indent=2)
        else:
            with open(path, 'w') as f:
                if isinstance(data, dict):
                    for k, v in data.items():
                        f.write(f"{k}: {v}\n")
                else:
                    f.write(str(data))
