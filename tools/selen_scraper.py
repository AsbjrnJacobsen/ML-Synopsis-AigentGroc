# tools/selen_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import json
import urllib.parse
from typing import List, Tuple, Optional
import os

def scrape_etilbudsavis(queries: List[str], save_dir: Optional[str] = None) -> Tuple[List[dict], str]:
    print("--------------Scraping Etilbudsavis--------------")
    all_products = []
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"scrape_resultat_{timestamp}.json"

    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        output_path = os.path.join(save_dir, filename)
    else:
        output_path = filename

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    for query in queries:
        url = f"https://etilbudsavis.dk/soeg/{urllib.parse.quote(query)}"
        driver.get(url)

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.flex.flex-col.overflow-hidden.text-ellipsis"))
            )
        except Exception as e:
            print(f"Timeout or error loading page for query: {query}", e)
            continue

        cards = driver.find_elements(By.CSS_SELECTOR, "div.flex.flex-col.overflow-hidden.text-ellipsis")
        print(f"[{query}] Antal kort fundet: {len(cards)}")

        for card in cards:
            try:
                navn_elem = card.find_element(By.CSS_SELECTOR, "h3")
                navn = navn_elem.text.strip() or navn_elem.get_attribute("innerText").strip()
                if not navn:
                    continue

                try:
                    pris = card.find_element(By.CSS_SELECTOR, "div.text-base").text.strip()
                except:
                    pris = ""

                try:
                    detaljer = card.find_element(By.CSS_SELECTOR, "p.text-xs").text.strip()
                except:
                    try:
                        detaljer = card.find_element(By.CSS_SELECTOR, "p.text-sm").text.strip()
                    except:
                        detaljer = ""

                try:
                    butik = card.find_element(By.CSS_SELECTOR, "div.rounded-lg.border").text.strip()
                except:
                    butik = ""

                try:
                    kampagnedato = card.find_element(By.CSS_SELECTOR, "div.flex-row.items-center.gap-1 p.text-xs").text.strip()
                except:
                    kampagnedato = ""

                all_products.append({
                    "navn": navn,
                    "pris": pris,
                    "detaljer": detaljer,
                    "butik": butik,
                    "kampagnedato": kampagnedato,
                    "scraped_at": datetime.datetime.now().isoformat()
                })

            except Exception as e:
                print("Fejl under parsing af kort:", e)
                print("Kortets HTML:", card.get_attribute("outerHTML"))
                continue

    driver.quit()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)

    print(f"Scraping done: {len(all_products)} produkter fundet totalt.")
    return all_products, output_path

if __name__ == "__main__":
    queries = ["mælk", "æg", "schulstad gulerodsrugbrød", "dadler"]
    results, output_path = scrape_etilbudsavis(queries)
    print(f"{len(results)} produkter gemt i: {output_path}")
