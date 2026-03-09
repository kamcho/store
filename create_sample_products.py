import os
import sys
import django

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Find the Django settings module
def find_settings():
    for item in os.listdir(BASE_DIR):
        if os.path.isdir(os.path.join(BASE_DIR, item)) and os.path.exists(os.path.join(BASE_DIR, item, 'settings.py')):
            return f"{item}.settings"
    return "Samsung.settings"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', find_settings())
django.setup()

from home.models import Product, ProductCategory

def create_products():
    # Create Categories
    tv_cat, _ = ProductCategory.objects.get_or_create(name='Home Entertainment', slug='home-entertainment')
    phone_cat, _ = ProductCategory.objects.get_or_create(name='Smartphone', slug='smartphone')
    watch_cat, _ = ProductCategory.objects.get_or_create(name='Wearable', slug='wearable')

    # Product 1: Neo QLED TV
    if not Product.objects.filter(model_code='QN900C').exists():
        p1 = Product(
            name='Neo QLED 8K',
            slug='neo-qled-8k',
            category=tv_cat,
            price=3499.00,
            description='Infinite screen with Neural Quantum Processor 8K for optimized picture quality.',
            series='Neo QLED',
            model_code='QN900C',
            is_active=True
        )
        # We won't download images here to avoid complexity/errors, just creating the data structure.
        # The template handles missing images gracefully.
        p1.save()
        print(f"Created {p1.name}")
    else:
        print("Neo QLED 8K already exists")

    # Product 2: Galaxy S24 Ultra
    if not Product.objects.filter(model_code='SM-S928').exists():
        p2 = Product(
            name='Galaxy S24 Ultra',
            slug='galaxy-s24-ultra',
            category=phone_cat,
            price=1299.00,
            description='Unleash your creativity, productivity, and possibility with the new era of mobile AI.',
            series='Galaxy S',
            model_code='SM-S928',
            is_active=True
        )
        p2.save()
        print(f"Created {p2.name}")
    else:
        print("Galaxy S24 Ultra already exists")

    # Product 3: Galaxy Watch 6
    if not Product.objects.filter(model_code='SM-R930').exists():
        p3 = Product(
            name='Galaxy Watch 6',
            slug='galaxy-watch-6',
            category=watch_cat,
            price=299.00,
            description='Start your everyday wellness journey with a classic look and advanced sleep coaching.',
            series='Galaxy Watch',
            model_code='SM-R930',
            is_active=True
        )
        p3.save()
        print(f"Created {p3.name}")
    else:
        print("Galaxy Watch 6 already exists")

if __name__ == '__main__':
    create_products()
