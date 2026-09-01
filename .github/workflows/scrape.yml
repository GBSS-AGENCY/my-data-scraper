import os
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Define target and dataset location
TARGET_URL = "https://quotes.toscrape.com/"  # Replace with your target website
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "dataset.csv")

def run_scraper():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(TARGET_URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch site: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all("div", class_="quote")
    
    os.makedirs(DATA_DIR, exist_ok=True)
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write header if file doesn't exist
        if not file_exists:
            writer.writerow(["Timestamp", "Text", "Author"])

        timestamp = datetime.utcnow().isoformat()
        
        for quote in quotes:
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            writer.writerow([timestamp, text, author])

    print("Scraping completed successfully.")

if __name__ == "__main__":
    run_scraper()
