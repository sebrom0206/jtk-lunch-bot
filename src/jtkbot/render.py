import random
from datetime import date

from jtkbot.models import DayDish

GREETINGS = [
    "Hei, Jesper her! I dag har jeg laget dette til deg:",
    "God morgen! Gjett hva jeg har trylla frem i dag:",
    "Jesper i køkkenet melder fra, dagens rett er klar:",
    "Sulten? Det bør du være, se hva jeg har laget:",
    "Moin! Her er dagens fra Jespers Torvekøkken:",
]

FRIDAY_GREETINGS = [
    "Endelig fredag! Her er ukens siste kreasjon:",
    "Fredag, og jeg har spart noe ekstra godt til deg:",
    "Siste dag før helg, la oss avslutte uken skikkelig:",
]


def _pick_greeting(weekday: str) -> str:
    if weekday.lower() == "fredag":
        return random.choice(FRIDAY_GREETINGS)
    return random.choice(GREETINGS)


def render_daily_email(week_data: dict[str, list[DayDish]]) -> tuple[str, str] | None:
    """Bygger emne og innhold for dagens e-post, basert på dagens dato.

    Returnerer None hvis det ikke finnes noen meny for i dag (helg,
    helligdag, eller uken som er lastet ikke dekker dagens dato).
    """
    today_str = date.today().strftime("%d-%m-%Y")

    lines: list[str] = []
    found_any = False
    weekday = ""

    for location, dishes in week_data.items():
        today_dish = next((d for d in dishes if d.date == today_str), None)
        if today_dish is None:
            continue
        if not found_any:
            weekday = today_dish.weekday
            lines.append(_pick_greeting(weekday))
            lines.append("")
        found_any = True
        lines.append(f"📍 {location}")
        lines.append(f"   {today_dish.dish}")
        lines.append("")

    if not found_any:
        return None

    subject = f"JTK Dagens rett – {weekday} {today_str}"
    body = "\n".join(lines).strip()
    return subject, body