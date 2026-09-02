import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime
import time

os.makedirs("data", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

def scrape_godot_api():
    filepath = "data/godot_assets.csv"
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Asset Name", "Creator", "Category", "Cost", "Direct Link"])
        try:
            url = "https://godotengine.org/asset-library/api/asset?max_results=2000"
            res = requests.get(url, headers=HEADERS, timeout=10)
            if res.status_code == 200:
                data = res.json().get("result", [])
                for item in data:
                    writer.writerow([
                        timestamp, item.get("title", "Unknown"), item.get("author", "Unknown"), 
                        item.get("category", "Uncategorized"), item.get("cost", "Unknown"), 
                        f"https://godotengine.org/asset-library/asset/{item.get('asset_id')}"
                    ])
                print(f"✅ Godot: Saved {len(data)} assets.")
        except Exception as e:
            print(f"⚠️ Godot scraper error: {e}")

def scrape_itchio():
    filepath = "data/itchio_assets.csv"
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Asset Title", "Creator", "Direct Link"])
        try:
            url = "https://itch.io/game-assets/free"
            res = requests.get(url, headers=HEADERS, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                cells = soup.find_all("div", class_="game_cell")
                for cell in cells:
                    title_tag = cell.find("a", class_="title")
                    author_tag = cell.find("div", class_="game_author")
                    if title_tag:
                        writer.writerow([
                            timestamp, title_tag.text.strip(), 
                            author_tag.text.strip() if author_tag else "Unknown", 
                            title_tag.get("href")
                        ])
                print(f"✅ Itch.io: Assets saved.")
        except Exception as e:
            print(f"⚠️ Itch.io scraper error: {e}")

def scrape_unity_store():
    filepath = "data/unity_assets.csv"
    # Create file first so Git always tracks it
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Asset Title", "Publisher", "Rating", "Direct Link"])
        try:
            url = "https://assetstore.unity.com/api/en-US/search/results.json?q=free&page=1&rows=100"
            res = requests.get(url, headers=HEADERS, timeout=10)
            if res.status_code == 200:
                data = res.json().get("results", [])
                for item in data:
                    writer.writerow([
                        timestamp, item.get("title", "Unknown"), 
                        item.get("publisher", {}).get("label", "Unknown"), 
                        item.get("rating", {}).get("average", "0"), 
                        f"https://assetstore.unity.com/packages/slug/{item.get('slug')}"
                    ])
                print(f"✅ Unity: Saved {len(data)} assets.")
            else:
                print(f"⚠️ Unity returned HTTP {res.status_code}. File structure created.")
        except Exception as e:
            print(f"⚠️ Unity scraper error: {e}")

def scrape_unreal_marketplace():
    filepath = "data/unreal_assets.csv"
    # Create file first so Git always tracks it
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Asset Title", "Developer", "Price", "Direct Link"])
        try:
            url = "https://www.unrealengine.com/marketplace/api/assets?max=100&start=0"
            res = requests.get(url, headers=HEADERS, timeout=10)
            if res.status_code == 200:
                data = res.json().get("data", {}).get("elements", [])
                for item in data:
                    writer.writerow([
                        timestamp, item.get("title", "Unknown"), 
                        item.get("developerDisplayName", "Unknown"), 
                        item.get("priceValue", "Free"), 
                        f"https://www.unrealengine.com/marketplace/en-US/product/{item.get('urlSlug')}"
                    ])
                print(f"✅ Unreal: Saved {len(data)} assets.")
            else:
                print(f"⚠️ Unreal returned HTTP {res.status_code}. File structure created.")
        except Exception as e:
            print(f"⚠️ Unreal scraper error: {e}")

if __name__ == "__main__":
    scrape_godot_api()
    time.sleep(2)
    scrape_itchio()
    time.sleep(2)
    scrape_unity_store()
    time.sleep(2)
    scrape_unreal_marketplace()
