import os
import django
import sys

# Setup Django environment
# Add the project root to sys.path so 'Samsung' module can be found
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Samsung.settings')
django.setup()

from home.models import ProductCategory
from django.utils.text import slugify

def get_or_create_category(name, parent=None):
    slug = slugify(name)
    # Handle duplicate slugs if necessary (though unique here)
    category, created = ProductCategory.objects.get_or_create(
        name=name,
        defaults={'slug': slug, 'parent': parent}
    )
    if not created and category.parent != parent:
        category.parent = parent
        category.save()
    return category

def populate():
    categories_structure = {
        "Mobile & Wearables": {
            "Smartphones": ["Galaxy S Series", "Galaxy Note Series", "Galaxy Z Series", "Galaxy A Series"],
            "Tablets": ["Galaxy Tab S Series", "Galaxy Tab A Series"],
            "Smartwatches & Wearables": ["Galaxy Watch Series", "Galaxy Fit & Bands"],
            "Mobile Accessories": ["Phone cases & covers", "Chargers & cables", "Earbuds (Galaxy Buds)"]
        },
        "TV & Audio": {
            "Televisions": ["QLED", "Crystal UHD", "Neo QLED", "Lifestyle TV"],
            "Home Audio": ["Soundbars", "Wireless speakers"],
            "TV Accessories": ["TV mounts", "Remote controls"]
        },
        "Home Appliances": {
            "Refrigerators": ["French Door", "Side-by-Side", "Top & Bottom Freezer"],
            "Washing Machines & Dryers": ["Front Load", "Top Load"],
            "Air Conditioners & Air Purifiers": [],
            "Microwaves & Ovens": [],
            "Vacuum Cleaners": ["Robot Vacuums", "Stick Vacuums"]
        },
        "Computing & Storage": {
            "Laptops": ["Galaxy Book Series", "Notebook Series"],
            "Monitors": [],
            "External Storage": ["SSDs", "Portable drives"],
            "Printers & Accessories": []
        },
        "Smart Home & IoT": {
            "SmartThings Devices": ["Smart cameras", "Smart plugs & sensors", "Smart lighting", "Smart home integration"]
        },
        "Cameras & Imaging": {}
    }

    for parent_name, subcategories in categories_structure.items():
        parent_cat = get_or_create_category(parent_name)
        print(f"Created/Verified parent category: {parent_name}")
        
        for sub_name, leaf_items in subcategories.items() if isinstance(subcategories, dict) else {}:
            sub_cat = get_or_create_category(sub_name, parent=parent_cat)
            print(f"  Created/Verified subcategory: {sub_name}")
            
            for leaf_name in leaf_items:
                leaf_cat = get_or_create_category(leaf_name, parent=sub_cat)
                print(f"    Created/Verified leaf category: {leaf_name}")

if __name__ == "__main__":
    populate()
    print("Population complete!")
