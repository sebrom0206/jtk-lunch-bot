import json
from dataclasses import asdict
from pathlib import Path

from jtkbot.models import DayDish

CACHE_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "week.json"


def save_week_menu(data: dict[str, list[DayDish]]) -> None:
    serializable = {
        location: [asdict(d) for d in dishes] for location, dishes in data.items()
    }
    CACHE_PATH.write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")


def load_week_menu() -> dict[str, list[DayDish]]:
    raw = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {
        location: [DayDish(**d) for d in dishes] for location, dishes in raw.items()
    }