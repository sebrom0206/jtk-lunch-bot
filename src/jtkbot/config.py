import os


def get_locations() -> dict[str, str]:
    """Returnerer {stedsnavn: value} basert på JTK_LOCATIONS i .env.

    Format i .env: JTK_LOCATIONS=16,2
    Navnene hentes fra denne faste mappingen, siden value-koden alene
    ikke er lesbar i selve dataen vi lagrer.
    """
    known = {
        "1": "Solbjerg Plads",
        "2": "Dalgas Have",
        "32": "Porcelænshaven",
        "16": "Kilen",
        "87": "Flintholm",
        "93": "Graduate House",
    }
    raw = os.environ["JTK_LOCATIONS"]
    values = [v.strip() for v in raw.split(",") if v.strip()]
    return {known[v]: v for v in values}