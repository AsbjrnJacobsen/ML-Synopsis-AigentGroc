# tools/price_optimizer.py

import json
from collections import defaultdict
from typing import List, Dict


def normalize_name(name: str) -> str:
    return name.lower().replace("\u00e6", "ae").replace("\u00f8", "oe").replace("\u00e5", "aa")


def find_best_prices(query_items: List[str], results: List[Dict], preferred_stores: List[str]) -> Dict[str, List[Dict]]:
    best_by_item = {}

    for item in query_items:
        item_norm = normalize_name(item)
        candidates = [r for r in results if item_norm in normalize_name(r["navn"])]

        if not candidates:
            best_by_item[item] = None
            continue

        # Find best price from preferred stores first
        preferred_candidates = [c for c in candidates if any(s.lower() in c["butik"].lower() for s in preferred_stores)]
        use_candidates = preferred_candidates if preferred_candidates else candidates

        # Pick lowest priced item (naive extraction assuming "10 kr" format)
        def extract_price(val):
            try:
                return float(val.lower().replace(" kr", "").replace(",", "."))
            except:
                return float("inf")

        best_offer = min(use_candidates, key=lambda x: extract_price(x["pris"]))
        best_by_item[item] = best_offer

    # Group results by store
    store_map = defaultdict(list)
    for item, offer in best_by_item.items():
        if offer:
            store_map[offer["butik"]].append(offer)

    return dict(store_map)


def generate_summary(store_map: Dict[str, List[Dict]], query_items: List[str], results: List[Dict]) -> str:
    lines = []
    found_items = set()

    for store, items in store_map.items():
        lines.append(f"From {store} you should buy:")
        for item in items:
            lines.append(f"{item['navn']}, {item['detaljer']}, {item['pris']}")
            found_items.add(item['navn'].lower())
        lines.append("")

    # Suggest future deals for missing items
    missing_items = [item for item in query_items if not any(normalize_name(item) in normalize_name(r['navn']) for r in results)]

    if missing_items:
        lines.append("\nNote that we couldn't find:")
        for item in missing_items:
            lines.append(f"- {item}")

    return "\n".join(lines)


def load_and_optimize(filename: str, items: List[str], preferred_stores: List[str]) -> str:
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    store_map = find_best_prices(items, data, preferred_stores)
    return generate_summary(store_map, items, data)


if __name__ == "__main__":
    # Example usage
    items = ["mælk", "æg", "schulstad gulerodsrugbrød", "dadler"]
    preferred = ["Netto", "fleggaard", "rema1000", "coop", "bilka", "føtex"]
    summary = load_and_optimize("scrape_resultat_dagligvarer.json", items, preferred)
    print(summary)
