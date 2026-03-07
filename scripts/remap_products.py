import os
import django
import sys

# Setup Django environment
sys.path.append('/home/kali/Downloads/Samsung')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Samsung.settings')
django.setup()

from home.models import Product, ProductCategory

def remap():
    remapping = {
        'smartphone': 'smartphones',
        'tvs': 'televisions',
        'wearable': 'smartwatches-wearables',
        'audio': 'home-audio',
        'computing': 'computing-storage',
        'appliances': 'home-appliances',
    }

    for old_slug, new_slug in remapping.items():
        try:
            old_cat = ProductCategory.objects.get(slug=old_slug)
            new_cat = ProductCategory.objects.get(slug=new_slug)
            
            products = Product.objects.filter(category=old_cat)
            count = products.count()
            if count > 0:
                products.update(category=new_cat)
                print(f"Remapped {count} products from '{old_cat.name}' to '{new_cat.name}'")
            
            # Delete old category if it's not the same as the new one
            if old_cat.pk != new_cat.pk:
                old_cat.delete()
                print(f"Deleted old category: '{old_cat.name}'")
        except ProductCategory.DoesNotExist:
            print(f"Category with slug '{old_slug}' or '{new_slug}' not found, skipping...")

if __name__ == "__main__":
    remap()
    print("Remapping complete!")
