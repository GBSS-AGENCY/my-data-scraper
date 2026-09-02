import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime
import time

# Initialize environment
os.makedirs("data", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Standard headers to mimic a real browser and prevent immediate bot-blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/html, */*"
}

def scrape_godot_api():
    print("Scraping Godot Asset Library...")
    url = "https://godotengine.org/asset-library/api/asset?max_results=2000"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json().get("result", [])
        filepath = "data/godot_assets.csv"
        
        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Asset Name", "Creator", "Category", "Cost", "Direct Link"])
            for item in data:
                writer.writerow([
                    timestamp, item.get("title", "Unknown"), item.get("author", "Unknown"), 
                    item.get("category", "Uncategorized"), item.get("cost", "Unknown"), 
                    f"https://godotengine.org/asset-library/asset/{item.get('asset_id')}"
                ])
        print(f"✅ Godot: Saved {len(data)} assets.")
    else:
        print(f"❌ Godot: Failed to fetch API (Status {response.status_code})")

def scrape_itchio():
    print("Scraping Itch.io Free Game Assets...")
    # Itch.io relies on HTML rendering, so we use BeautifulSoup
    url = "https://itch.io/game-assets/free"
    response = requests.get(url, headers=HEADERS)
    assets_found = 0
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        filepath = "data/itchio_assets.csv"
        
        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Asset Title", "Creator", "Direct Link"])
            
            # Find all game cards on the page
            game_cells = soup.find_all("div", class_="game_cell")
            for cell in game_cells:
                title_tag = cell.find("a", class_="title")
                author_tag = cell.find("div", class_="game_author")
                
                if title_tag:
                    title = title_tag.text.strip()
                    link = title_tag.get("href")
                    author = author_tag.text.strip() if author_tag else "Unknown"
                    
                    writer.writerow([timestamp, title, author, link])
                    assets_found += 1
                    
        print(f"✅ Itch.io: Saved {assets_found} top free assets.")
    else:
        print(f"❌ Itch.io: Failed to load page (Status {response.status_code})")

def scrape_unity_store():
    print("Scraping Unity Asset Store (via Search Endpoint)...")
    # Using Unity's backend JSON search endpoint for free assets
    url = "https://assetstore.unity.com/api/en-US/search/results.json?q=free&page=1&rows=100"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        try:
            data = response.json().get("results", [])
            filepath = "data/unity_assets.csv"
            
            with open(filepath, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Asset Title", "Publisher", "Rating", "Direct Link"])
                
                for item in data:
                    title = item.get("title", "Unknown")
                    publisher = item.get("publisher", {}).get("label", "Unknown")
                    rating = item.get("rating", {}).get("average", "0")
                    link = f"https://assetstore.unity.com/packages/slug/{item.get('slug')}"
                    
                    writer.writerow([timestamp, title, publisher, rating, link])
            print(f"✅ Unity: Saved {len(data)} assets.")
        except Exception as e:
            print(f"❌ Unity: JSON Parsing error - {e}")
    else:
        print(f"❌ Unity: Request blocked or failed (Status {response.status_code})")

def scrape_unreal_marketplace():
    print("Scraping Unreal Engine Marketplace (Epic Games)...")
    # Unreal's marketplace is heavily JavaScript-rendered and protected.
    # We hit their catalog search API endpoint directly to bypass JS loading.
    url = "https://www.unrealengine.com/marketplace/api/assets?max=100&start=0&sortBy=effectiveDate&sortDir=DESC"
    
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        try:
            data = response.json().get("data", {}).get("elements", [])
            filepath = "data/unreal_assets.csv"
            
            with open(filepath, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Asset Title", "Developer", "Price", "Direct Link"])
                
                for item in data:
                    title = item.get("title", "Unknown")
                    developer = item.get("developerDisplayName", "Unknown")
                    price = item.get("priceValue", "Unknown")
                    link = f"https://www.unrealengine.com/marketplace/en-US/product/{item.get('urlSlug')}"
                    
                    writer.writerow([timestamp, title, developer, price, link])
            print(f"✅ Unreal: Saved {len(data)} assets.")
        except Exception as e:
             print(f"❌ Unreal: JSON Parsing error - {e}")
    else:
        print(f"❌ Unreal: Epic blocked the automated request (Status {response.status_code}). Note: Epic uses strict Cloudflare rules on some servers.")

if __name__ == "__main__":
    print(f"--- Starting Scraping Run at {timestamp} ---")
    scrape_godot_api()
    time.sleep(2) # Pauses between requests to prevent IP throttling
    scrape_itchio()
    time.sleep(2)
    scrape_unity_store()
    time.sleep(2)
    scrape_unreal_marketplace()
    print("--- Run Complete! Dataset folder is updated. ---")
