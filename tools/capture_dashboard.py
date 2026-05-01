from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "projects" / "agent-dashboard" / "index.html"
OUT = ROOT / "proof" / "screenshots" / "agent-dashboard.png"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1100}, device_scale_factor=1)
        page.goto(HTML.as_uri(), wait_until="networkidle")
        page.screenshot(path=str(OUT), full_page=True)
        browser.close()
    print(OUT)


if __name__ == "__main__":
    main()
