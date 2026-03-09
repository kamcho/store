import setup_django

from django.db import transaction
from home.models import Product, ProductVariant

def add_gear360_variants():
    product = Product.objects.get(slug='sm-r210')
    
    # Check existing variants
    existing_variants = ProductVariant.objects.filter(product=product)
    print(f"Current variants for {product.name}: {existing_variants.count()}")
    
    with transaction.atomic():
        # Add more variants for Gear 360
        variants_data = [
            {
                'name': 'Gear 360 Camera - 32GB',
                'model_code': 'SM-R210-32GB',
                'price': 349.99,
                'sale_price': 299.99,
                'cost_price': 200.00,
                'stock_quantity': 25,
                'min_stock_level': 5,
                'availability': 'in_stock',
                'is_active': True,
                'specifications': {
                    'storage': '32GB',
                    'resolution': '15MP',
                    'video_quality': '4K',
                    'battery_life': 'Up to 2 hours',
                    'connectivity': 'Bluetooth 4.1, Wi-Fi'
                }
            },
            {
                'name': 'Gear 360 Camera - 64GB',
                'model_code': 'SM-R210-64GB',
                'price': 449.99,
                'sale_price': 399.99,
                'cost_price': 250.00,
                'stock_quantity': 15,
                'min_stock_level': 5,
                'availability': 'in_stock',
                'is_active': True,
                'specifications': {
                    'storage': '64GB',
                    'resolution': '15MP',
                    'video_quality': '4K',
                    'battery_life': 'Up to 2 hours',
                    'connectivity': 'Bluetooth 4.1, Wi-Fi'
                }
            },
            {
                'name': 'Gear 360 Camera - Professional Kit',
                'model_code': 'SM-R210-PRO',
                'price': 599.99,
                'sale_price': 549.99,
                'cost_price': 350.00,
                'stock_quantity': 8,
                'min_stock_level': 3,
                'availability': 'in_stock',
                'is_active': True,
                'specifications': {
                    'storage': '64GB',
                    'resolution': '15MP',
                    'video_quality': '4K',
                    'battery_life': 'Up to 4 hours with extra battery',
                    'connectivity': 'Bluetooth 4.1, Wi-Fi',
                    'includes': 'Extra battery, Tripod mount, Carrying case'
                }
            }
        ]
        
        for variant_data in variants_data:
            # Check if variant already exists
            existing = ProductVariant.objects.filter(
                product=product, 
                model_code=variant_data['model_code']
            ).first()
            
            if existing:
                print(f"⚠️  Variant {variant_data['name']} already exists, skipping...")
                continue
            
            # Create new variant
            variant = ProductVariant.objects.create(
                product=product,
                **variant_data
            )
            print(f"✅ Created variant: {variant.name}")
    
    # Verify
    total_variants = ProductVariant.objects.filter(product=product).count()
    print(f"🎉 Total variants for {product.name}: {total_variants}")

if __name__ == "__main__":
    add_gear360_variants()
