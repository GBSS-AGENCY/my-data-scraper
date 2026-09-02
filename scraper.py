import os
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Target Itch.io Game Assets filtered by Godot
BASE_URL = "https://itch.io/game-assets/tag-godot?page={}"
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "godot_assets_dataset.csv")

def run_scraper():
    os.makedirs(DATA_DIR, exist_ok=True)
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Asset Title", "Creator", "Link"])

        page = 1
        total_scraped = 0
        
        while page <= 50: # Limit to 50 pages (approx 1,500 assets) for safety
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(BASE_URL.format(page), headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find the asset cards on Itch.io
            assets = soup.find_all("div", class_="game_cell")
            
            if not assets:
                break 

            timestamp = datetime.utcnow().isoformat()
            
            for asset in assets:
                title_tag = asset.find("a", class_="title")
                creator_tag = asset.find("a", class_="author")
                
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag.get("href")
                    creator = creator_tag.get_text(strip=True) if creator_tag else "Unknown"
                    
                    writer.writerow([timestamp, title, creator, link])
                    total_scraped += 1
            
            print(f"Scraped page {page}")
            page += 1
            time.sleep(2) # 2-second delay is crucial so you don't get blocked

    print(f"Success: Added {total_scraped} rows.")

if __name__ == "__main__":
    run_scraper()
