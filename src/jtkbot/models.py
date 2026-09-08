from dataclasses import dataclass


@dataclass
class DayDish:
    date: str       # "07-09-2026"
    weekday: str    # "Mandag"
    dish: str       # "Kylling Tikka Masala med fladbrød, ris, raita og koriander"