# scrape_ibapi.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

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
            data.append({
                "Property Title": cols[0].text.strip(),
                "Bank": cols[1].text.strip(),
                "City": cols[2].text.strip(),
                "State": cols[3].text.strip(),
                "Pincode": cols[4].text.strip(),
                "Auction Date": cols[5].text.strip(),
                "Details URL": "https://ibapi.in/" + cols[9].find("a")["href"] if cols[9].find("a") else ""
            })

    df = pd.DataFrame(data)
    filename = f"properties_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved {len(df)} listings to {filename}")
