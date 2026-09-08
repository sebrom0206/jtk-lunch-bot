import re
import time

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from jtkbot.config import get_locations
from jtkbot.models import DayDish

BASE_URL = "https://jtkmenu.torvekoekken.dk/1"
DATE_PATTERN = re.compile(r"(\d{2}-\d{2}-\d{4})\s*-\s*(\w+)")


def _extract_dishes_for_location(page) -> list[DayDish] | None:
    """Leser 'Dagens ret' for hver dag. Returnerer None hvis siden var
    midt i en re-render (elementer forsvant under lesing)."""
    try:
        dishes: list[DayDish] = []
        cards = page.locator("#contentToPrint .card:visible").all()

        for card in cards:
            header_text = card.locator(".card-header").inner_text(timeout=3000)
            match = DATE_PATTERN.search(header_text)
            if not match:
                continue
            date_str, weekday = match.group(1), match.group(2)

            headers = card.locator(".menu_header_ny").all()
            rets = card.locator(".menu_ret_ny").all()

            dish_text = None
            for i, h in enumerate(headers):
                if h.inner_text(timeout=3000).strip() == "Dagens ret":
                    if i < len(rets):
                        dish_text = rets[i].inner_text(timeout=3000).strip()
                    break

            if dish_text:
                dishes.append(DayDish(date=date_str, weekday=weekday, dish=dish_text))

        return dishes
    except PlaywrightTimeoutError:
        return None  # siden var ustabil akkurat da, prøv igjen


def _wait_for_content_change(page, previous_first_dish: str | None, timeout_ms=15000) -> list[DayDish]:
    start = time.monotonic()
    while (time.monotonic() - start) * 1000 < timeout_ms:
        dishes = _extract_dishes_for_location(page)
        if dishes:
            current_first = dishes[0].dish
            if current_first != previous_first_dish:
                return dishes
        page.wait_for_timeout(400)
    return _extract_dishes_for_location(page) or []


def fetch_week_menu() -> dict[str, list[DayDish]]:
    locations = get_locations()
    result: dict[str, list[DayDish]] = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(BASE_URL)
        page.wait_for_selector("select.form-select")
        page.wait_for_timeout(2000)

        location_select = page.locator("select.form-select").nth(0)
        previous_dish = None

        for name, value in locations.items():
            location_select.select_option(value=value)
            dishes = _wait_for_content_change(page, previous_dish)
            result[name] = dishes
            previous_dish = dishes[0].dish if dishes else previous_dish

        browser.close()

    return result