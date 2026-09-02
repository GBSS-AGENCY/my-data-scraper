import os
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

BASE_URL = "https://quotes.toscrape.com/page/{}/"
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "dataset.csv")

def run_scraper():
    os.makedirs(DATA_DIR, exist_ok=True)
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Text", "Author"])

        page = 1
        total_scraped = 0
        
        while True:
            # Fetch the current page
            response = requests.get(BASE_URL.format(page))
            soup = BeautifulSoup(response.text, "html.parser")
            quotes = soup.find_all("div", class_="quote")
            
            # If no quotes are found, we've reached the end
            if not quotes:
                break 

            timestamp = datetime.utcnow().isoformat()
            
            for quote in quotes:
                text = quote.find("span", class_="text").get_text(strip=True)
                author = quote.find("small", class_="author").get_text(strip=True)
                writer.writerow([timestamp, text, author])
                total_scraped += 1
            
            print(f"Scraped page {page}")
            page += 1
            time.sleep(1) # Polite delay to avoid overloading the server

    print(f"Success: Added {total_scraped} rows.")

if __name__ == "__main__":
    run_scraper()
