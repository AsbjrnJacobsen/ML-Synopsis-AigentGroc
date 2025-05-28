# Agent Design: Grocery Shopping Assistant

## Overview
This agent is a grocery shopping assistant powered by `pyautogen` and an LLM (e.g., `mistral:latest`). Its purpose is to help users find the best current deals on grocery items using real data from the Danish website etilbudsavis.dk.

## Core Components

### Agents
- `GroceryAssistant` (`AssistantAgent`): The LLM-powered assistant responsible for interpreting user requests and triggering the tool.
- `UserProxy` (`UserProxyAgent`): The user interface component which executes the tool function when instructed.

### Tool: `selen_scraper.py` Function: `scrape_etilbudsavis`
- This function scrapes live data from etilbudsavis.dk using Selenium.
- It retrieves current offers for grocery items, finds the best price from preferred stores, and summarizes the result.
- JSON data is saved in the `/data/` directory for traceability.

## Instructions to the LLM
The system message ensures:
- The assistant **never guesses** prices or store names.
- It **always calls the tool**, even if the item seems unusual.
- Only real tool output is used in responses.

## Flow
1. User sends prompt: e.g. "Find mælk og æg"
2. Assistant calls the tool `scrape_etilbudsavis` with parsed items.
3. Tool fetches data and returns structured response.
4. Assistant replies with a list of cheapest stores and saves results.
"""

# Use Cases

## Case 1: Common Items

**Input Prompt:**
```
Find mælk og æg
```

**Expected Output:**
```
🔎 28 resultater fundet.

From Lidl you should buy:
- Arla Mælk, 1L, 6.95 kr
From Føtex you should buy:
- Øko Æg, 6 stk, 11.00 kr

📁 Resultaterne er gemt i: data/scrape_resultat_*.json
```

## Case 2: Multiple Items

**Input Prompt:**
```
rugbrød, makrel, havregryn
```

**Expected Output:**
A list of best offers per product across preferred stores. Includes fallback if items are missing.

## Case 3: Unknown Item

**Input Prompt:**
```
enhjørningekage
```

**Expected Output:**
```
❌ Ingen resultater fundet.
```


# Aigent Grocery Shopping Assistant

This project implements a grocery shopping assistant powered by an LLM and the `pyautogen` framework. It helps users find the cheapest groceries by scraping live offers from etilbudsavis.dk.

## 💡 Features

- Search for grocery deals using real data
- Tool-assisted agent (no hallucination)
- Store preferences and price comparison
- JSON output saved for every search

## 🚀 Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Run the Agent
```bash
python agent/grocery_agent.py
```

## 🧰 Requirements

- Python 3.10+
- Chrome + chromedriver (installed via `webdriver-manager`)
- Ollama (running `mistral:latest` or similar)

## 📁 Folder Structure

- `agent/`: Core agent logic
- `tools/`: Scraper and price optimizer
- `config/`: LLM config file
- `data/`: Saved JSON search results

