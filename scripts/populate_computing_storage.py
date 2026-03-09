#!/usr/bin/env python3
"""
Script to populate Computing & Storage products
"""

import os, sys, django
sys.path.append('/home/kali/Downloads/Samsung')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Samsung.settings')
django.setup()

from django.db import transaction
from home.models import ProductCategory, Product, ProductVariant, ProductSpecification

def create_computing_storage():
    # Categories
    laptop_cat, _ = ProductCategory.objects.get_or_create(name="Laptops", defaults={'slug': 'laptops'})
    monitor_cat, _ = ProductCategory.objects.get_or_create(name="Monitors", defaults={'slug': 'monitors'})
    storage_cat, _ = ProductCategory.objects.get_or_create(name="External Storage", defaults={'slug': 'external-storage'})
    printer_cat, _ = ProductCategory.objects.get_or_create(name="Printers & Accessories", defaults={'slug': 'printers-accessories'})

    # Laptops - Galaxy Book Series
    laptop_products = [
        {
            'name': 'Samsung Galaxy Book Pro 360',
            'model_code': 'NP930QED',
            'category': laptop_cat,
            'variants': [
                {
                    'name': '13.3" Intel Core i7 16GB 512GB',
                    'model_code': 'NP930QED-13I7',
                    'price': 1499.99,
                    'specs': {
                        'screen_size': '13.3 inch',
                        'processor': 'Intel Core i7-1165G7',
                        'memory': '16GB LPDDR4x',
                        'storage': '512GB NVMe SSD',
                        'display': 'FHD AMOLED Touch',
                        'graphics': 'Intel Iris Xe',
                        'battery': '68Wh',
                        'weight': '1.04kg',
                        'features': '360° Flip, S Pen, Thunderbolt 4'
                    }
                },
                {
                    'name': '15.6" Intel Core i7 16GB 1TB',
                    'model_code': 'NP950QED-15I7',
                    'price': 1799.99,
                    'specs': {
                        'screen_size': '15.6 inch',
                        'processor': 'Intel Core i7-1165G7',
                        'memory': '16GB LPDDR4x',
                        'storage': '1TB NVMe SSD',
                        'display': 'FHD Super AMOLED Touch',
                        'graphics': 'Intel Iris Xe',
                        'battery': '68Wh',
                        'weight': '1.41kg',
                        'features': '360° Flip, S Pen, Thunderbolt 4'
                    }
                }
            ]
        },
        {
            'name': 'Samsung Galaxy Book3 Pro',
            'model_code': 'NP950XED',
            'category': laptop_cat,
            'variants': [
                {
                    'name': '14" Intel Core i5 8GB 256GB',
                    'model_code': 'NP940XED-14I5',
                    'price': 1199.99,
                    'specs': {
                        'screen_size': '14 inch',
                        'processor': 'Intel Core i5-1335U',
                        'memory': '8GB LPDDR5',
                        'storage': '256GB NVMe SSD',
                        'display': 'FHD+ Dynamic AMOLED 2X',
                        'graphics': 'Intel Iris Xe',
                        'battery': '63Wh',
                        'weight': '1.17kg',
                        'features': 'AKG Speakers, Thunderbolt 4, Fingerprint'
                    }
                },
                {
                    'name': '16" Intel Core i7 16GB 512GB',
                    'model_code': 'NP960XED-16I7',
                    'price': 1599.99,
                    'specs': {
                        'screen_size': '16 inch',
                        'processor': 'Intel Core i7-1360P',
                        'memory': '16GB LPDDR5',
                        'storage': '512GB NVMe SSD',
                        'display': 'FHD+ Dynamic AMOLED 2X',
                        'graphics': 'Intel Iris Xe',
                        'battery': '76Wh',
                        'weight': '1.56kg',
                        'features': 'AKG Speakers, Thunderbolt 4, Fingerprint, NumberPad'
                    }
                }
            ]
        },
        {
            'name': 'Samsung Galaxy Book3 Ultra',
            'model_code': 'NP960XFG',
            'category': laptop_cat,
            'variants': [
                {
                    'name': '16" Intel Core i7 16GB 1TB RTX 4050',
                    'model_code': 'NP960XFG-16I7',
                    'price': 2199.99,
                    'specs': {
                        'screen_size': '16 inch',
                        'processor': 'Intel Core i7-13700H',
                        'memory': '16GB LPDDR5',
                        'storage': '1TB NVMe SSD',
                        'display': '2.8K Dynamic AMOLED 2X 120Hz',
                        'graphics': 'NVIDIA RTX 4050 6GB',
                        'battery': '76Wh',
                        'weight': '1.79kg',
                        'features': 'Gaming, Thunderbolt 4, RGB Keyboard, Vapor Chamber'
                    }
                },
                {
                    'name': '16" Intel Core i9 32GB 2TB RTX 4070',
                    'model_code': 'NP960XFG-16I9',
                    'price': 2799.99,
                    'specs': {
                        'screen_size': '16 inch',
                        'processor': 'Intel Core i9-13900H',
                        'memory': '32GB LPDDR5',
                        'storage': '2TB NVMe SSD',
                        'display': '2.8K Dynamic AMOLED 2X 120Hz',
                        'graphics': 'NVIDIA RTX 4070 8GB',
                        'battery': '76Wh',
                        'weight': '1.79kg',
                        'features': 'Gaming, Thunderbolt 4, RGB Keyboard, Vapor Chamber'
                    }
                }
            ]
        }
    ]

    # Monitors
    monitor_products = [
        {
            'name': 'Samsung Odyssey OLED G8',
            'model_code': 'LS34CG850S',
            'category': monitor_cat,
            'variants': [
                {
                    'name': '34" Curved OLED 240Hz Gaming Monitor',
                    'model_code': 'LS34CG850S-34',
                    'price': 1499.99,
                    'specs': {
                        'screen_size': '34 inch',
                        'panel_type': 'QHD OLED',
                        'resolution': '3440x1440',
                        'refresh_rate': '240Hz',
                        'response_time': '0.1ms GtG',
                        'curvature': '1800R',
                        'brightness': '250 nits',
                        'contrast_ratio': '1,000,000:1',
                        'features': 'HDR10+, G-Sync, FreeSync Premium Pro, USB Hub'
                    }
                }
            ]
        },
        {
            'name': 'Samsung Smart Monitor M8',
            'model_code': 'LS27BM800U',
            'category': monitor_cat,
            'variants': [
                {
                    'name': '27" 4K UHD Smart Monitor',
                    'model_code': 'LS27BM800U-27',
                    'price': 699.99,
                    'specs': {
                        'screen_size': '27 inch',
                        'panel_type': 'IPS',
                        'resolution': '3840x2160 (4K UHD)',
                        'refresh_rate': '60Hz',
                        'response_time': '4ms',
                        'brightness': '300 nits',
                        'color_gamut': '99% sRGB',
                        'features': 'Smart TV, Remote Control, Wireless DeX, USB-C Hub, Built-in Apps'
                    }
                },
                {
                    'name': '32" 4K UHD Smart Monitor',
                    'model_code': 'LS32BM800U-32',
                    'price': 899.99,
                    'specs': {
                        'screen_size': '32 inch',
                        'panel_type': 'VA',
                        'resolution': '3840x2160 (4K UHD)',
                        'refresh_rate': '60Hz',
                        'response_time': '5ms',
                        'brightness': '300 nits',
                        'contrast_ratio': '3000:1',
                        'features': 'Smart TV, Remote Control, Wireless DeX, USB-C Hub, Built-in Apps'
                    }
                }
            ]
        },
        {
            'name': 'Samsung ViewFinity S9',
            'model_code': 'LS27C900PA',
            'category': monitor_cat,
            'variants': [
                {
                    'name': '27" 5K Professional Monitor',
                    'model_code': 'LS27C900PA-27',
                    'price': 1599.99,
                    'specs': {
                        'screen_size': '27 inch',
                        'panel_type': 'IPS',
                        'resolution': '5120x2880 (5K)',
                        'refresh_rate': '60Hz',
                        'response_time': '5ms',
                        'brightness': '600 nits',
                        'color_accuracy': 'ΔE<2',
                        'features': 'Thunderbolt 4, Color Calibration, Matte Display, Height Adjustable'
                    }
                }
            ]
        }
    ]

    # External Storage
    storage_products = [
        {
            'name': 'Samsung T7 Portable SSD',
            'model_code': 'MU-PC500T',
            'category': storage_cat,
            'variants': [
                {
                    'name': '500GB Portable SSD',
                    'model_code': 'MU-PC500T-500',
                    'price': 79.99,
                    'specs': {
                        'capacity': '500GB',
                        'interface': 'USB 3.2 Gen 2',
                        'read_speed': '1050 MB/s',
                        'write_speed': '1000 MB/s',
                        'form_factor': 'Portable',
                        'encryption': 'AES 256-bit',
                        'features': 'Shock Resistant, Metal Body, Compact Size'
                    }
                },
                {
                    'name': '1TB Portable SSD',
                    'model_code': 'MU-PC1T0-1TB',
                    'price': 129.99,
                    'specs': {
                        'capacity': '1TB',
                        'interface': 'USB 3.2 Gen 2',
                        'read_speed': '1050 MB/s',
                        'write_speed': '1000 MB/s',
                        'form_factor': 'Portable',
                        'encryption': 'AES 256-bit',
                        'features': 'Shock Resistant, Metal Body, Compact Size'
                    }
                },
                {
                    'name': '2TB Portable SSD',
                    'model_code': 'MU-PC2T0-2TB',
                    'price': 199.99,
                    'specs': {
                        'capacity': '2TB',
                        'interface': 'USB 3.2 Gen 2',
                        'read_speed': '1050 MB/s',
                        'write_speed': '1000 MB/s',
                        'form_factor': 'Portable',
                        'encryption': 'AES 256-bit',
                        'features': 'Shock Resistant, Metal Body, Compact Size'
                    }
                }
            ]
        },
        {
            'name': 'Samsung 980 PRO NVMe SSD',
            'model_code': 'MZ-V8P1T0B',
            'category': storage_cat,
            'variants': [
                {
                    'name': '1TB NVMe M.2 SSD',
                    'model_code': 'MZ-V8P1T0-1TB',
                    'price': 149.99,
                    'specs': {
                        'capacity': '1TB',
                        'interface': 'PCIe 4.0 NVMe',
                        'read_speed': '7000 MB/s',
                        'write_speed': '5000 MB/s',
                        'form_factor': 'M.2 2280',
                        'endurance': '600 TBW',
                        'features': 'DRAM Cache, PCIe Gen4, High Performance'
                    }
                },
                {
                    'name': '2TB NVMe M.2 SSD',
                    'model_code': 'MZ-V8P2T0-2TB',
                    'price': 249.99,
                    'specs': {
                        'capacity': '2TB',
                        'interface': 'PCIe 4.0 NVMe',
                        'read_speed': '7000 MB/s',
                        'write_speed': '5000 MB/s',
                        'form_factor': 'M.2 2280',
                        'endurance': '1200 TBW',
                        'features': 'DRAM Cache, PCIe Gen4, High Performance'
                    }
                }
            ]
        },
        {
            'name': 'Samsung T7 Shield Portable SSD',
            'model_code': 'MU-PE500S',
            'category': storage_cat,
            'variants': [
                {
                    'name': '1TB Rugged Portable SSD',
                    'model_code': 'MU-PE1T0-1TB',
                    'price': 159.99,
                    'specs': {
                        'capacity': '1TB',
                        'interface': 'USB 3.2 Gen 2',
                        'read_speed': '1050 MB/s',
                        'write_speed': '1000 MB/s',
                        'form_factor': 'Portable',
                        'protection': 'IP65, Drop to 3m',
                        'features': 'Water Resistant, Dust Proof, Shock Resistant, Rubber Guard'
                    }
                },
                {
                    'name': '2TB Rugged Portable SSD',
                    'model_code': 'MU-PE2T0-2TB',
                    'price': 249.99,
                    'specs': {
                        'capacity': '2TB',
                        'interface': 'USB 3.2 Gen 2',
                        'read_speed': '1050 MB/s',
                        'write_speed': '1000 MB/s',
                        'form_factor': 'Portable',
                        'protection': 'IP65, Drop to 3m',
                        'features': 'Water Resistant, Dust Proof, Shock Resistant, Rubber Guard'
                    }
                }
            ]
        }
    ]

    # Printers & Accessories
    printer_products = [
        {
            'name': 'Samsung Xpress M2070FW Laser Printer',
            'model_code': 'SL-M2070FW',
            'category': printer_cat,
            'variants': [
                {
                    'name': 'All-in-One Wireless Laser Printer',
                    'model_code': 'SL-M2070FW-AIO',
                    'price': 299.99,
                    'specs': {
                        'type': 'Monochrome Laser All-in-One',
                        'functions': 'Print, Copy, Scan, Fax',
                        'print_speed': '21 ppm',
                        'resolution': '1200 x 1200 dpi',
                        'connectivity': 'Wi-Fi, Ethernet, USB',
                        'paper_capacity': '150 sheets',
                        'features': 'Mobile Printing, NFC, Eco Mode'
                    }
                }
            ]
        },
        {
            'name': 'Samsung MultiXpress SL-M3320ND',
            'model_code': 'SL-M3320ND',
            'category': printer_cat,
            'variants': [
                {
                    'name': 'Monochrome Laser Printer',
                    'model_code': 'SL-M3320ND-LASER',
                    'price': 399.99,
                    'specs': {
                        'type': 'Monochrome Laser',
                        'functions': 'Print Only',
                        'print_speed': '33 ppm',
                        'resolution': '1200 x 1200 dpi',
                        'connectivity': 'USB, Ethernet',
                        'paper_capacity': '250 sheets',
                        'features': 'Duplex Printing, High Volume, Business Use'
                    }
                }
            ]
        },
        {
            'name': 'Samsung Toner Cartridges',
            'model_code': 'MLT-D203L',
            'category': printer_cat,
            'variants': [
                {
                    'name': 'Black Toner Cartridge Standard',
                    'model_code': 'MLT-D203L-STD',
                    'price': 89.99,
                    'specs': {
                        'type': 'Black Toner Cartridge',
                        'page_yield': '2500 pages',
                        'compatibility': 'Xpress M2070 Series',
                        'color': 'Black',
                        'features': 'OEM, High Yield, Easy Installation'
                    }
                },
                {
                    'name': 'Black Toner Cartridge High Yield',
                    'model_code': 'MLT-D203L-HIGH',
                    'price': 129.99,
                    'specs': {
                        'type': 'Black Toner Cartridge',
                        'page_yield': '5000 pages',
                        'compatibility': 'Xpress M2070 Series',
                        'color': 'Black',
                        'features': 'OEM, Extra High Yield, Easy Installation'
                    }
                }
            ]
        }
    ]

    all_products = laptop_products + monitor_products + storage_products + printer_products

    with transaction.atomic():
        for product_data in all_products:
            product = Product.objects.create(
                name=product_data['name'],
                slug=f"{product_data['model_code'].lower()}",
                description=f"Premium {product_data['name']} with advanced features and cutting-edge technology",
                short_description=f"High-performance {product_data['name']} for professionals and enthusiasts",
                warranty_period=24,
                features=['Smart Technology', 'Energy Efficient', 'Professional Grade', 'Warranty Support'],
                category=product_data['category'],
                is_featured=True if 'Galaxy Book3 Ultra' in product_data['name'] or 'Odyssey' in product_data['name'] else False,
                is_active=True
            )
            
            for variant_data in product_data['variants']:
                variant = ProductVariant.objects.create(
                    product=product,
                    name=variant_data['name'],
                    model_code=variant_data['model_code'],
                    price=variant_data['price'],
                    stock_quantity=25,
                    min_stock_level=5,
                    availability='in_stock',
                    specifications=variant_data['specs'],
                    is_active=True
                )
                
                spec_order = 0
                for spec_key, spec_value in variant_data['specs'].items():
                    ProductSpecification.objects.create(
                        product=product,
                        category=spec_key,
                        name=spec_key,
                        value=str(spec_value),
                        display_order=spec_order
                    )
                    spec_order += 1
            
            print(f"✅ Created {product_data['name']}")

    print(f"🎉 Created {len(all_products)} Computing & Storage products!")
    print(f"💻 Total variants: {sum(len(p['variants']) for p in all_products)}")

if __name__ == "__main__":
    create_computing_storage()
