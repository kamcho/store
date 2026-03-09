#!/usr/bin/env python3
"""
Script to populate Home Appliances products
"""

import os, sys, django
sys.path.append('/home/kali/Downloads/Samsung')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Samsung.settings')
django.setup()

from django.db import transaction
from home.models import ProductCategory, Product, ProductVariant, ProductSpecification

def create_home_appliances():
    # Categories
    fridge_cat, _ = ProductCategory.objects.get_or_create(name="Refrigerators", defaults={'slug': 'refrigerators'})
    washer_cat, _ = ProductCategory.objects.get_or_create(name="Washing Machines & Dryers", defaults={'slug': 'washing-machines-dryers'})
    ac_cat, _ = ProductCategory.objects.get_or_create(name="Air Conditioners & Air Purifiers", defaults={'slug': 'air-conditioners-purifiers'})
    microwave_cat, _ = ProductCategory.objects.get_or_create(name="Microwaves & Ovens", defaults={'slug': 'microwaves-ovens'})
    vacuum_cat, _ = ProductCategory.objects.get_or_create(name="Vacuum Cleaners", defaults={'slug': 'vacuum-cleaners'})

    # Refrigerators
    fridge_products = [
        {
            'name': 'Samsung Family Hub French Door Refrigerator',
            'model_code': 'RF28R7351SR',
            'category': fridge_cat,
            'variants': [
                {'name': '28 cu ft French Door', 'model_code': 'RF28R7351SR-28', 'price': 3499.99, 'specs': {'capacity': '28 cu ft', 'type': 'French Door', 'features': 'Family Hub, Ice & Water'}},
                {'name': '29 cu ft French Door', 'model_code': 'RF28R7351SR-29', 'price': 3799.99, 'specs': {'capacity': '29 cu ft', 'type': 'French Door', 'features': 'Family Hub, Ice & Water'}}
            ]
        },
        {
            'name': 'Samsung Side-by-Side Refrigerator',
            'model_code': 'RS27T5561SR',
            'category': fridge_cat,
            'variants': [
                {'name': '27 cu ft Side-by-Side', 'model_code': 'RS27T5561SR-27', 'price': 2299.99, 'specs': {'capacity': '27 cu ft', 'type': 'Side-by-Side', 'features': 'Ice & Water, Smart Cooling'}}
            ]
        }
    ]

    # Washing Machines
    washer_products = [
        {
            'name': 'Samsung Front Load Washer',
            'model_code': 'WF45B6300AW',
            'category': washer_cat,
            'variants': [
                {'name': '4.5 cu ft Front Load', 'model_code': 'WF45B6300AW-45', 'price': 999.99, 'specs': {'capacity': '4.5 cu ft', 'type': 'Front Load', 'features': 'SmartThings, Steam'}}
            ]
        },
        {
            'name': 'Samsung Top Load Washer',
            'model_code': 'WA50R5400AV',
            'category': washer_cat,
            'variants': [
                {'name': '5.0 cu ft Top Load', 'model_code': 'WA50R5400AV-50', 'price': 799.99, 'specs': {'capacity': '5.0 cu ft', 'type': 'Top Load', 'features': 'ActiveWave, Smart Control'}}
            ]
        }
    ]

    # Air Conditioners
    ac_products = [
        {
            'name': 'Samsung WindFree AC',
            'model_code': 'AR12TXEAAWK',
            'category': ac_cat,
            'variants': [
                {'name': '12000 BTU WindFree', 'model_code': 'AR12TXEAAWK-12', 'price': 1299.99, 'specs': {'capacity': '12000 BTU', 'type': 'Split AC', 'features': 'WindFree, Smart Control'}}
            ]
        }
    ]

    # Microwaves
    microwave_products = [
        {
            'name': 'Samsung Smart Microwave',
            'model_code': 'ME18R7040FS',
            'category': microwave_cat,
            'variants': [
                {'name': '1.8 cu ft Microwave', 'model_code': 'ME18R7040FS-18', 'price': 299.99, 'specs': {'capacity': '1.8 cu ft', 'type': 'Countertop', 'features': 'Smart Sensor, Ceramic Enamel'}}
            ]
        }
    ]

    # Vacuums
    vacuum_products = [
        {
            'name': 'Samsung Robot Vacuum',
            'model_code': 'VR20T6030WW',
            'category': vacuum_cat,
            'variants': [
                {'name': 'Robot Vacuum+', 'model_code': 'VR20T6030WW-ROBOT', 'price': 699.99, 'specs': {'type': 'Robot', 'features': 'LiDAR, Smart Mapping'}}
            ]
        }
    ]

    all_products = fridge_products + washer_products + ac_products + microwave_products + vacuum_products

    with transaction.atomic():
        for product_data in all_products:
            product = Product.objects.create(
                name=product_data['name'],
                slug=f"{product_data['model_code'].lower()}",
                description=f"Premium {product_data['name']} with advanced features",
                short_description=f"High-quality {product_data['name']}",
                warranty_period=24,
                features=['Smart Control', 'Energy Efficient', 'Quiet Operation'],
                category=product_data['category'],
                is_active=True
            )
            
            for variant_data in product_data['variants']:
                variant = ProductVariant.objects.create(
                    product=product,
                    name=variant_data['name'],
                    model_code=variant_data['model_code'],
                    price=variant_data['price'],
                    stock_quantity=20,
                    min_stock_level=5,
                    availability='in_stock',
                    specifications=variant_data['specs'],
                    is_active=True
                )
                
                for spec_key, spec_value in variant_data['specs'].items():
                    ProductSpecification.objects.create(
                        product=product,
                        category=spec_key,
                        name=spec_key,
                        value=spec_value,
                        display_order=0
                    )
            
            print(f"✅ Created {product_data['name']}")

    print(f"🎉 Created {len(all_products)} Home Appliances products!")

if __name__ == "__main__":
    create_home_appliances()
