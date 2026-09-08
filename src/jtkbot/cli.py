import sys

from dotenv import load_dotenv

load_dotenv()

from jtkbot.fetch import fetch_week_menu
from jtkbot.cache import save_week_menu, load_week_menu
from jtkbot.render import render_daily_email
from jtkbot.deliver import send_email


def scrape() -> None:
    """Henter hele ukens meny og lagrer til data/week.json. Kjøres mandager."""
    data = fetch_week_menu()
    save_week_menu(data)
    total = sum(len(dishes) for dishes in data.values())
    print(f"Scraped {len(data)} steder, {total} dager totalt. Lagret til data/week.json")


def send() -> None:
    """Leser data/week.json og sender dagens meny på e-post. Kjøres hverdager."""
    data = load_week_menu()
    result = render_daily_email(data)
    if result is None:
        print("Ingen meny funnet for i dag, hopper over utsendelse.")
        return
    subject, body = result
    send_email(subject, body)
    print(f"Sendt: {subject}")


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ("scrape", "send"):
        print("Bruk: python -m jtkbot.cli scrape | send")
        sys.exit(1)

    if sys.argv[1] == "scrape":
        scrape()
    else:
        send()


if __name__ == "__main__":
    main()