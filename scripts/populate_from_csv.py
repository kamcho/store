import sys
import os
import setup_django
import csv
import requests
import re
from django.db import transaction
from django.utils.text import slugify
from home.models import ProductCategory, Product, ProductVariant, ProductImage, ProductSpecification

# CSV file path - Now using the enriched version
CSV_FILE = "samsung_full_products.csv"

# Global system encoding for printing to console safely
SYS_ENCODING = sys.stdout.encoding or 'utf-8'

def safe_print(msg):
    """Prints message by encoding to system encoding and ignoring errors for terminal compatibility"""
    try:
        print(msg.encode(SYS_ENCODING, errors='replace').decode(SYS_ENCODING))
    except:
        print(msg) # Fallback to standard print

def get_or_create_nested_category(category_path):
    """Helper to create nested categories from a list of names"""
    parent = None
    last_cat = None
    for cat_name in category_path:
        last_cat, _ = ProductCategory.objects.get_or_create(
            name=cat_name,
            parent=parent,
            defaults={'slug': slugify(cat_name)}
        )
        parent = last_cat
    return last_cat

def map_category(product_name):
    """Maps product name to category hierarchy based on keywords"""
    name_upper = product_name.upper()
    
    # TV & Audio 
    if "TV" in name_upper:
        if "NEO QLED" in name_upper:
            return ["TV & Audio", "Televisions", "Neo QLED"]
        if "QLED" in name_upper:
            return ["TV & Audio", "Televisions", "QLED"]
        if "OLED" in name_upper:
            return ["TV & Audio", "Televisions", "OLED"]
        if "UHD" in name_upper or "4K" in name_upper or "LED" in name_upper:
            return ["TV & Audio", "Televisions", "Crystal UHD"]
        return ["TV & Audio", "Televisions"]
    
    if "SOUND BAR" in name_upper or "SOUNDBAR" in name_upper or "SPEAKER" in name_upper:
        return ["TV & Audio", "Home Audio"]
    
    # Home Appliances
    if "WASHING MACHINE" in name_upper or "WASHER" in name_upper or "DRYER" in name_upper:
        if "FRONT LOAD" in name_upper:
            return ["Home Appliances", "Washing Machines & Dryers", "Front Load"]
        if "TOP LOAD" in name_upper:
            return ["Home Appliances", "Washing Machines & Dryers", "Top Load"]
        return ["Home Appliances", "Washing Machines & Dryers"]
    
    if "REFRIGERATOR" in name_upper or "FRIDGE" in name_upper:
        if "SIDE BY SIDE" in name_upper:
            return ["Home Appliances", "Refrigerators", "Side-by-Side"]
        if "DOUBLE DOOR" in name_upper or "TOP MOUNT" in name_upper:
            return ["Home Appliances", "Refrigerators", "Top & Bottom Freezer"]
        return ["Home Appliances", "Refrigerators"]
    
    if "FREEZER" in name_upper:
        return ["Home Appliances", "Refrigerators", "Chest Freezer"]
    
    if "COOKER" in name_upper or "HOB" in name_upper or "OVEN" in name_upper or "HOOD" in name_upper:
        return ["Home Appliances", "Kitchen Appliances", "Cookers"]
    
    if "MICROWAVE" in name_upper:
        return ["Home Appliances", "Kitchen Appliances", "Microwaves"]
    
    if "DISHWASHER" in name_upper:
        return ["Home Appliances", "Kitchen Appliances", "Dishwashers"]

    if "VACUUM" in name_upper or "VALET" in name_upper:
        return ["Home Appliances", "Cleaning Appliances"]

    if "AIR CONDITIONER" in name_upper or "AIRCONDITIONER" in name_upper:
        return ["Home Appliances", "Air Conditioning"]

    return ["Uncategorized"]

def populate(wipe_existing=False):
    safe_print(f"--- Starting population from enriched CSV ({CSV_FILE}) ---")
    
    abs_path = os.path.abspath(CSV_FILE)
    safe_print(f"Looking for CSV at: {abs_path}")

    if wipe_existing:
        safe_print("Wiping existing products...")
        Product.objects.all().delete()

    try:
        # Use utf-8-sig to handle potential BOM
        with open(CSV_FILE, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            count = 0
            success_count = 0
            
            # Check headers
            safe_print(f"Headers found: {reader.fieldnames}")
            if not reader.fieldnames:
                safe_print("Critical: No headers found in CSV.")
                return

            for row in reader:
                count += 1
                try:
                    name = row['Name']
                    # Cleanup price string more carefully
                    price_str = row['Price'].replace('KSh', '').replace(',', '').replace('.00', '').strip()
                    try:
                        price = float(price_str)
                    except ValueError:
                        price = 0.0
                    
                    image_url = row['Image']
                    description = row.get('Description', f"Product details for {name}")
                    spec_str = row.get('Specification', '')
                    
                    safe_print(f"Processing ({count}): {name}")
                    
                    cat_path = map_category(name)
                    category = get_or_create_nested_category(cat_path)
                    
                    with transaction.atomic():
                        # Create or update Product
                        product, created = Product.objects.update_or_create(
                            name=name,
                            defaults={
                                'category': category,
                                'description': description,
                                'short_description': name[:245],
                                'slug': slugify(name)[:50]
                            }
                        )
                        
                        # Create Variant
                        variant_name = "Default"
                        size_match = re.search(r'(\d+)["”]', name)
                        if size_match:
                            variant_name = f"{size_match.group(1)}-inch"

                        # Generate unique model code if not exists
                        model_code = None
                        if spec_str:
                            # Try to find model code in specs first
                            mc_match = re.search(r'Model Code:?\s?([^;]+)', spec_str, re.I)
                            if mc_match:
                                model_code = mc_match.group(1).strip()
                            else:
                                # Try one more pattern for model code (often at end of name)
                                name_mc_match = re.search(r':\s?([A-Z0-9\-]+)$', name)
                                if name_mc_match:
                                    model_code = name_mc_match.group(1)
                        
                        if not model_code:
                            base_model_code = slugify(name)[:40].upper()
                            model_code = base_model_code
                            suffix = 1
                            while ProductVariant.objects.filter(model_code=model_code).exclude(product=product).exists():
                                model_code = f"{base_model_code[:35]}-{suffix}"
                                suffix += 1

                        variant, _ = ProductVariant.objects.update_or_create(
                            product=product,
                            name=variant_name,
                            defaults={
                                'price': price,
                                'model_code': model_code,
                                'stock_quantity': 15,
                                'availability': 'in_stock'
                            }
                        )
                        
                        # Handle Image
                        if image_url:
                            try:
                                from django.core.files.base import ContentFile
                                img_response = requests.get(image_url, timeout=10)
                                if img_response.status_code == 200:
                                    img_name = f"{slugify(name)[:30]}.jpg"
                                    product_image, pi_created = ProductImage.objects.get_or_create(
                                        product=product,
                                        is_main_image=True,
                                        defaults={'alt_text': name[:200]}
                                    )
                                    product_image.image.save(img_name, ContentFile(img_response.content), save=True)
                            except Exception as img_err:
                                safe_print(f"  Warning: Skipping image for {name}: {img_err}")
                        
                        # Handle Specs and Features
                        if spec_str:
                            spec_parts = spec_str.split(';')
                            for part in spec_parts:
                                part = part.strip()
                                if not part: continue
                                
                                if ':' in part:
                                    s_key, s_val = part.split(':', 1)
                                    ProductSpecification.objects.update_or_create(
                                        product=product,
                                        name=s_key.strip()[:100],
                                        defaults={'value': s_val.strip()}
                                    )
                                else:
                                    # If no colon, save as a feature
                                    # Use a generic key or just use the part as the key with "Yes" as value
                                    # Given the user's example, it might be better to treat it as a "Characteristic"
                                    ProductSpecification.objects.update_or_create(
                                        product=product,
                                        name=part[:100],
                                        defaults={'value': 'Yes'}
                                    )
                        
                    success_count += 1

                except Exception as item_err:
                    safe_print(f"  Error processing item {count}: {item_err}")

            safe_print(f"--- Population completed! {success_count}/{count} products processed. ---")

    except FileNotFoundError:
        safe_print(f"Critical Error: {abs_path} not found.")
    except Exception as e:
        safe_print(f"Critical Unexpected error: {e}")

if __name__ == "__main__":
    # You can set wipe_existing=True if you want to start fresh
    populate(wipe_existing=True)
