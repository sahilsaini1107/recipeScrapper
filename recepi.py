# import required modules
from bs4 import BeautifulSoup
import requests
import csv

urls = [
    "https://en.wikibooks.org/wiki/Cookbook:Agar_Jelly",
    "https://en.wikibooks.org/wiki/Cookbook:Coconut_Pudding_I"
]

csv_file = "output.csv"
# Initialize an empty dictionary to hold the data
additems = {}
additems["Recipe"] = []
additems["Category"] = []

def scrape_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract data and fill the dictionary
        recipe = soup.tbody.tr.th.string
        category = soup.tbody.tr.next_sibling.td.string
        
        additems["Recipe"].append(recipe)
        additems["Category"].append(category)
        
        # Collect all H2 headers and their next sibling content
        headelements = soup.find_all('h2', limit=2)
        for head in headelements:
            header = head.span.text
            content = head.find_next_sibling().text
            if header not in additems:
                additems[header] = []
            additems[header].append(content)
        
        print(additems)
    else:
        print(f"Failed to retrieve {url}")

# Scrape all URLs
for url in urls:
    scrape_url(url)

# Write the data to the CSV file
# Define the order of columns
fieldnames = list(additems.keys())

with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    # Create a CSV DictWriter object
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write the rows
    for i in range(len(additems["Recipe"])):
        row = {key: additems[key][i] if i < len(additems[key]) else '' for key in fieldnames}
        writer.writerow(row)
