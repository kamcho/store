import os
import django
import sys

# Setup Django environment
BASE_DIR = '/home/kali/Downloads/Samsung'
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Samsung.settings')
django.setup()

from home.models import Product, ProductVariant

def migrate_data():
    products = Product.objects.all()
    print(f"Total products to process: {products.count()}")
    
    for p in products:
        # Check if it already has variants
        if p.variants.exists():
            print(f"Skipping {p.name} - already has variants.")
            continue
            
        # Create a default variant
        variant = ProductVariant.objects.create(
            product=p,
            name="Standard", # Or use size if it's a TV, but for now Standard is safe
            model_code=p.model_code,
            price=p.price,
            sale_price=p.sale_price,
            cost_price=p.cost_price,
            stock_quantity=p.stock_quantity,
            min_stock_level=p.min_stock_level,
            availability=p.availability,
            is_active=p.is_active
        )
        print(f"Created default variant for {p.name}: {variant.model_code}")

if __name__ == '__main__':
    migrate_data()
    print("Data migration completed.")
