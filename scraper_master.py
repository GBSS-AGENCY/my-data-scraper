from curl_cffi import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime
import time

os.makedirs("data", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}

def scrape_godot_api():
    filepath = "data/godot_assets.csv"
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Asset Name", "Creator", "Category", "Cost", "Direct Link"])
        try:
            url = "https://godotengine.org/asset-library/api/asset?max_results=2000"
            res = requests.get(url, headers=HEADERS, impersonate="chrome120", timeout=15)
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
            print(f"⚠️ Godot error: {e}")

def scrape_itchio():
    filepath = "data/itchio_assets.csv"
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Asset Title", "Creator", "Direct Link"])
        total_saved = 0
        
        # Paginate across first 5 pages
        for page in range(1, 6):
            try:
                url = f"https://itch.io/game-assets/free?page={page}"
                res = requests.get(url, headers=HEADERS, impersonate="chrome120", timeout=15)
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
                            total_saved += 1
                time.sleep(1)
            except Exception as e:
                print(f"⚠️ Itch.io page {page} error: {e}")
        print(f"✅ Itch.io: Saved {total_saved} total assets across 5 pages.")

def scrape_unity_assets():
    filepath = "data/unity_assets.csv"
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Asset Title", "Platform Tag", "Direct Link"])
        total_saved = 0
        
        # Paginate Unity-tagged assets across 8 pages
        for page in range(1, 9):
            try:
                url = f"https://itch.io/game-assets/tag-unity/free?page={page}"
                res = requests.get(url, headers=HEADERS, impersonate="chrome120", timeout=15)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    cells = soup.find_all("div", class_="game_cell")
                    for cell in cells:
                        title_tag = cell.find("a", class_="title")
                        if title_tag:
                            writer.writerow([
                                timestamp, title_tag.text.strip(), 
                                "Unity Compatible", title_tag.get("href")
                            ])
                            total_saved += 1
                time.sleep(1)
            except Exception as e:
                print(f"⚠️ Unity page {page} error: {e}")
        print(f"✅ Unity Engine: Saved {total_saved} assets across 8 pages.")

def scrape_unreal_engine():
    filepath = "data/unreal_assets.csv"
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Asset Title", "Platform Tag", "Direct Link"])
        total_saved = 0
        
        # Paginate Unreal-tagged assets across 8 pages
        for page in range(1, 9):
            try:
                url = f"https://itch.io/game-assets/tag-unreal-engine/free?page={page}"
                res = requests.get(url, headers=HEADERS, impersonate="chrome120", timeout=15)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    cells = soup.find_all("div", class_="game_cell")
                    for cell in cells:
                        title_tag = cell.find("a", class_="title")
                        if title_tag:
                            writer.writerow([
                                timestamp, title_tag.text.strip(), 
                                "Unreal Engine Compatible", title_tag.get("href")
                            ])
                            total_saved += 1
                time.sleep(1)
            except Exception as e:
                print(f"⚠️ Unreal page {page} error: {e}")
        print(f"✅ Unreal Engine: Saved {total_saved} assets across 8 pages.")

if __name__ == "__main__":
    print(f"--- Launching Scaled Multi-Page Extraction at {timestamp} ---")
    scrape_godot_api()
    scrape_itchio()
    scrape_unity_assets()
    scrape_unreal_engine()
    print("--- Scraping Complete! All 4 CSVs updated. ---")
