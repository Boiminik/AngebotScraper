import asyncio
import json
import os
import datetime
from playwright.async_api import async_playwright


async def scrape_billa(base_url, brand_name, kw, year, city="wien", output_file="billa_output.json"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Erste Seite aufrufen, um max. Seitenzahl zu holen
        url = f"{base_url}/{brand_name}_fb_kw{kw}_{year}_{city}/page/1"
        await page.goto(url)

        # Max Seiten auslesen
        total_pages_text = await page.locator("div#progress_indicator span.total").inner_text()
        total_pages = int(total_pages_text.strip())
        # Max Seiten ausgeben
        print(f"[INFO] {brand_name}: max. Seitenanzahl = {total_pages}")

        data = []
        i = 1
        # Schleife für den durchlauf aller Seiten, i wird inkrementiert
        while i <= total_pages:
            page_url = f"{base_url}/{brand_name}_fb_kw{kw}_{year}_{city}/page/{i}"
            await page.goto(page_url)
            await page.wait_for_load_state("domcontentloaded")

            # Aktuelles Slide
            current_slide = page.locator("div.slide.reader-view.current")

            # Warte auf left-img
            await current_slide.locator("img.left").first.wait_for(timeout=10000)

            # Page-Numbers checken (einzeln oder doppelseite)
            page_numbers_text = await page.locator("span.page-numbers").inner_text()
            page_numbers_text = page_numbers_text.strip()

            # Links/Rechts alt-Text holen
            left_alt = await current_slide.locator("img.left").first.get_attribute("alt")
            right_locator = current_slide.locator("img.right").first
            right_handle = await right_locator.element_handle()
            right_alt = None
            if right_handle:
                right_alt = await right_locator.get_attribute("alt")

            # JSON-Einträge
            # Prüfe, ob Doppel-Seite (z.B. "2-3")
            if "-" in page_numbers_text and right_alt:
                left_page = page_numbers_text.split("-")[0].strip()
                right_page = page_numbers_text.split("-")[1].strip()

                # Seite links
                data.append({
                    "seite": left_page,
                    "produkte": left_alt.split("\n") if left_alt else [],
                    "url": f"{base_url}/{brand_name}_fb_kw{kw}_{year}_{city}/page/{left_page}"
                })

                # Seite rechts
                data.append({
                    "seite": right_page,
                    "produkte": right_alt.split("\n") if right_alt else [],
                    "url": f"{base_url}/{brand_name}_fb_kw{kw}_{year}_{city}/page/{right_page}"
                })

                i += 2  # nächstes Doppel-Page
            else:
                # Einzel-Seite
                data.append({
                    "seite": page_numbers_text,
                    "produkte": left_alt.split("\n") if left_alt else [],
                    "url": f"{base_url}/{brand_name}_fb_kw{kw}_{year}_{city}/page/{i}"
                })
                i += 1

        # JSON speichern
        os.makedirs("archiv/billa", exist_ok=True)
        os.makedirs("archiv/billa-plus", exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        await browser.close()
        print(f"[INFO] Fertig! Daten gespeichert in {output_file}")


if __name__ == "__main__":
    # Kalenderwoche bestimmen
    today = datetime.date.today()
    # zfill um einstellige ziffern zweistellig zu machen
    kw = str(today.isocalendar()[1]).zfill(2)
    # aktuelles Jahr
    year = today.year

    # URLs
    billa_url = "https://view.publitas.com/billa-at"
    billa_plus_url = "https://view.publitas.com/billa-plus"

    # Scrape Funktion für Billa ausführen
    asyncio.run(scrape_billa(billa_url, "Billa", kw, year, output_file=f"archiv/billa/billa_kw{kw}_{year}.json"))

    # Scrape Funktion für Billa Plus ausführen
    asyncio.run(scrape_billa(billa_plus_url, "Billa Plus", kw, year, output_file=f"archiv/billa-plus/billa-plus_kw{kw}_{year}.json"))
