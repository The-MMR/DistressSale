import requests
from bs4 import BeautifulSoup
from google.cloud import firestore
from datetime import datetime
import os

def scrape_ibapi():
    print("🔍 Scraping IBAPI...")

    url = "https://ibapi.in/SearchPropertyDetails.jsp"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", class_="table table-bordered table-striped")

    if not table:
        print("❌ No table found.")
        return

    rows = table.find_all("tr")[1:]
    data = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 10:
            item = {
                "PropertyTitle": cols[0].text.strip(),
                "Bank": cols[1].text.strip(),
                "City": cols[2].text.strip(),
                "State": cols[3].text.strip(),
                "Pincode": cols[4].text.strip(),
                "AuctionDate": cols[5].text.strip(),
                "DetailsURL": "https://ibapi.in/" + cols[9].find("a")["href"] if cols[9].find("a") else "",
                "scraped_at": datetime.utcnow().isoformat()
            }
            data.append(item)

    # Firestore: connect
    db = firestore.Client()

    for item in data:
        # Unique document ID based on URL or property title
        doc_id = item["DetailsURL"].split('=')[-1] if item["DetailsURL"] else item["PropertyTitle"].replace(" ", "_")
        db.collection("properties").document(doc_id).set(item)

    print(f"✅ Uploaded {len(data)} properties to Firestore.")

if __name__ == "__main__":
    scrape_ibapi()
