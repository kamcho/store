import requests
import csv
import html

# API endpoint for Samsung products
API_URL = "https://samsutech.net/wp-json/wc/store/products?category=samsung&per_page=100"

# output CSV file
OUTPUT_FILE = "samsung_products.csv"


def scrape_products():
    print(f"Fetching products from: {API_URL}")
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        products = response.json()
    except Exception as e:
        print(f"Error fetching products: {e}")
        return

    print(f"Found {len(products)} total items. Filtering for Samsung products...")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Add URL column
        writer.writerow(["Name", "Price", "Image", "URL"])

        count = 0
        for product in products:
            name_raw = product.get("name", "N/A")
            # Unescape HTML entities like &#8243;
            name = html.unescape(name_raw)
            
            # Local filter for "SAMSUNG" in name, as a safeguard
            if "SAMSUNG" not in name.upper():
                continue

            # Format price
            prices = product.get("prices", {})
            price_val = prices.get("price", "0")
            currency = prices.get("currency_symbol", "KSh")
            
            try:
                # Assuming price in cents
                formatted_price = f"{currency}{int(price_val)/100:,.2f}"
            except (ValueError, TypeError):
                formatted_price = f"{currency}{price_val}"

            # Get image
            image_url = ""
            images = product.get("images", [])
            if images:
                image_url = images[0].get("src", "")

            # Get product URL
            product_url = product.get("permalink", "")

            writer.writerow([name, formatted_price, image_url, product_url])
            count += 1

    print(f"\nFinished. {count} Samsung products saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape_products()