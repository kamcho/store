import sys
import requests
from bs4 import BeautifulSoup
import csv
import time

input_file = 'samsung_products.csv'
output_file = 'samsung_full_products.csv'

# Common headers to avoid blocks
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Global system encoding for printing to console safely
SYS_ENCODING = sys.stdout.encoding or 'utf-8'

def safe_print(msg):
    """Prints message by encoding to system encoding and ignoring errors for terminal compatibility"""
    try:
        print(msg.encode(SYS_ENCODING, errors='replace').decode(SYS_ENCODING))
    except:
        print(msg) # Fallback to standard print

products = []
with open(input_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        products.append(row)

safe_print(f"Found {len(products)} products to scrape detail pages...")

fieldnames = ['Name', 'Price', 'Image', 'URL', 'Description', 'Specification']

session = requests.Session()

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for idx, product in enumerate(products, 1):
        name = product['Name']
        price = product['Price']
        image = product['Image']
        url = product.get('URL')

        safe_print(f"Scraping ({idx}/{len(products)}): {name}")

        description = ''
        specification = ''

        if url:
            try:
                response = session.get(url, headers=HEADERS, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # 1. Description logic
                desc_div = soup.find('div', id='tab-description')
                if desc_div:
                    # Remove the "Description" header if it exists
                    h2 = desc_div.find('h2')
                    if h2: h2.decompose()
                    description = desc_div.get_text(separator=' ', strip=True)
                else:
                    fallback_desc = soup.find('div', class_='product-content')
                    if fallback_desc:
                        description = fallback_desc.get_text(separator=' ', strip=True)

                # 2. Specifications logic
                spec_panel = soup.find('div', id='tab-specifications')
                if spec_panel:
                    # Filter out nested description div if it exists inside spec_panel
                    nested_desc = spec_panel.find('div', id='tab-description')
                    if nested_desc: nested_desc.decompose()
                    
                    # Try table first
                    spec_table = spec_panel.find('table', class_='shop_attributes')
                    if spec_table:
                        specs = []
                        for row_spec in spec_table.find_all('tr'):
                            th = row_spec.find('th')
                            td = row_spec.find('td')
                            th_text = th.get_text(strip=True) if th else ''
                            td_text = td.get_text(strip=True) if td else ''
                            if th_text or td_text:
                                specs.append(f"{th_text}: {td_text}")
                        specification = '; '.join(specs)
                    else:
                        # Fallback to list/bullet points if no table
                        ul = spec_panel.find('ul')
                        if ul:
                            specification = '; '.join([li.get_text(strip=True) for li in ul.find_all('li')])
                        else:
                            # Final fallback: just get the text
                            specification = spec_panel.get_text(separator='; ', strip=True)
                
                # Cleanup: remove the "Specifications" title from the text if it was grabbed
                if specification.startswith("Specifications;"):
                    specification = specification[15:].strip()

            except Exception as e:
                safe_print(f"Error scraping {url}: {e}")

        writer.writerow({
            'Name': name,
            'Price': price,
            'Image': image,
            'URL': url,
            'Description': description,
            'Specification': specification
        })

        # Add a small delay
        time.sleep(0.5)

safe_print(f"\nScraping completed! Full product details saved to {output_file}")
