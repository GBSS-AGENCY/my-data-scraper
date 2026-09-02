import requests
import csv
import os
from datetime import datetime

# Initialize the central data directory
os.makedirs("data", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def scrape_godot_api():
    print("Fetching 1,800+ Godot resources via REST API...")
    url = "https://godotengine.org/asset-library/api/asset?max_results=2000"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json().get("result", [])
        with open("data/godot_assets_dataset.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Asset Name", "Creator", "Category", "License", "Direct Link"])
            
            for item in data:
                writer.writerow([
                    timestamp, 
                    item.get("title", "Unknown"), 
                    item.get("author", "Unknown"), 
                    item.get("category", "Uncategorized"), 
                    item.get("cost", "Unknown"), 
                    f"https://godotengine.org/asset-library/asset/{item.get('asset_id')}"
                ])
        print("Godot dataset updated successfully.")

def build_itchio_structure():
    # Itch.io uses heavy HTML elements. This creates the structural dataset 
    # ready for the BeautifulSoup parsing logic.
    print("Generating Itch.io framework...")
    with open("data/itchio_assets.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Asset Title", "Tags", "Price", "Direct Link"])

def build_commercial_engine_structure():
    # Unity & Unreal require dynamic scraping tools like Selenium due to GraphQL and JavaScript rendering.
    print("Generating Unity & Unreal framework...")
    engines = ["unity", "unreal"]
    for engine in engines:
        with open(f"data/{engine}_assets.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Asset Title", "Publisher", "Engine Version", "Direct Link"])

if __name__ == "__main__":
    scrape_godot_api()
    build_itchio_structure()
    build_commercial_engine_structure()
    print("All datasets processed and saved to the /data folder.")
