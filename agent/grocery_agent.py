from autogen import AssistantAgent, UserProxyAgent, register_function
import sys
import os
import time
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.selen_scraper import scrape_etilbudsavis
from tools.price_optimizer import find_best_prices, generate_summary
from config.llm_config import llm_config

# Create agents
user_proxy = UserProxyAgent(
    name="UserProxy",
    llm_config=llm_config,
    code_execution_config=False
)

grocery_agent = AssistantAgent(
    name="GroceryAssistant",
    llm_config=llm_config,
    system_message="""
    Du er en hjælpsom AI-indkøbsassistent. Du **MÅ IKKE** svare på noget uden først at bruge værktøjet `scrape_etilbudsavis`.

    **Du må ALDRIG gætte priser eller butikker. Brug KUN data fra værktøjet.**

    Instruktion:
    - Når brugeren nævner dagligvarer, kald `scrape_etilbudsavis`
    - Returnér KUN de data, du har fået fra værktøjet
    - Hvis ingen resultater findes, sig det ærligt
    - Du skal ALTID kalde værktøjet — også hvis du tror varen ikke findes
    - Du må ikke gentage tidligere forespørgsler medmindre brugeren eksplicit beder om det
    """
)

# Tool function
def scrape_etilbudsavis(query: str) -> str:
    print(f"[TOOL] Received query: {query}")
    queries = [q.strip() for q in query.split(",") if q.strip()]
    print(f"[TOOL] Parsed queries: {queries}")
    print("[DEBUG] Starting scrape...")
    time.sleep(2)  # Simulate tool delay for realism

    # Ensure output is saved in root/data folder
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    # Tell scraper where to save
    results, output_path = scrape_etilbudsavis(queries, save_dir=data_dir)

    if not results:
        return "❌ Ingen resultater fundet."

    preferred_stores = ["Netto", "Rema 1000", "Coop", "Bilka", "Føtex", "Lidl"]
    store_map = find_best_prices(queries, results, preferred_stores)
    summary = generate_summary(store_map, queries, results)

    return f"""🔎 {len(results)} resultater fundet.

{summary}

📁 Resultaterne er gemt i: {output_path}
"""


def main():
    register_function(
        scrape_etilbudsavis,
        caller=grocery_agent,
        executor=grocery_agent,
        description="Søg dagligvarepriser på etilbudsavis.dk med en søgeforespørgsel (f.eks. 'mælk', 'kaffe')"
    )

    user_proxy.initiate_chat(
        grocery_agent,
        message="Find kun de faktiske tilbud på dagligvarer fra etilbudsavis.dk. Brug værktøjet."
    )


if __name__ == "__main__":
    main()
