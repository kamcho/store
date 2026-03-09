import setup_django

from django.db import transaction
from home.models import ProductCategory, Product, ProductVariant, ProductSpecification

def create_cameras_imaging():
    # Create parent category first
    parent_cat, _ = ProductCategory.objects.get_or_create(name="Cameras & Imaging", defaults={'slug': 'cameras-imaging'})
    
    # Subcategories under Cameras & Imaging
    camera_cat, _ = ProductCategory.objects.get_or_create(name="Digital Cameras", defaults={'slug': 'digital-cameras', 'parent': parent_cat})
    lens_cat, _ = ProductCategory.objects.get_or_create(name="Camera Lenses", defaults={'slug': 'camera-lenses', 'parent': parent_cat})
    accessories_cat, _ = ProductCategory.objects.get_or_create(name="Camera Accessories", defaults={'slug': 'camera-accessories', 'parent': parent_cat})
    action_cam_cat, _ = ProductCategory.objects.get_or_create(name="Action Cameras", defaults={'slug': 'action-cameras', 'parent': parent_cat})

    # Digital Cameras
    camera_products = [
        {
            'name': 'Samsung Galaxy Camera 2',
            'model_code': 'EK-GC200',
            'category': camera_cat,
            'variants': [
                {
                    'name': '16.3MP Smart Camera',
                    'model_code': 'EK-GC200-16MP',
                    'price': 449.99,
                    'specs': {
                        'sensor': '16.3MP 1/2.3" BSI CMOS',
                        'lens': '21x optical zoom (23-483mm)',
                        'aperture': 'f/2.8 - 5.9',
                        'iso_range': '100 - 3200',
                        'video': '1080p @ 60fps',
                        'display': '4.8" HD Super Clear Touch LCD',
                        'connectivity': 'Wi-Fi, Bluetooth, NFC',
                        'storage': 'microSD up to 64GB',
                        'features': 'Android 4.3 Jelly Bean, Smart Mode, Photo Wizard'
                    }
                }
            ]
        },
        {
            'name': 'Samsung NX500 Mirrorless Camera',
            'model_code': 'EV-NX500',
            'category': camera_cat,
            'variants': [
                {
                    'name': '28MP Mirrorless Camera',
                    'model_code': 'EV-NX500-28MP',
                    'price': 799.99,
                    'specs': {
                        'sensor': '28MP APS-C BSI CMOS',
                        'lens_mount': 'Samsung NX-mount',
                        'iso_range': '100 - 51200',
                        'video': '4K UHD @ 30fps',
                        'display': '3.0" Super AMOLED touchscreen',
                        'viewfinder': 'Electronic (2.36M dots)',
                        'autofocus': '205-point phase detection',
                        'burst_shooting': '9 fps',
                        'connectivity': 'Wi-Fi, Bluetooth, NFC',
                        'features': 'DRIMe V Image Processor, HDR, Time-lapse'
                    }
                }
            ]
        },
        {
            'name': 'Samsung NX1 Mirrorless Camera',
            'model_code': 'EV-NX1',
            'category': camera_cat,
            'variants': [
                {
                    'name': '28.2MP Professional Mirrorless',
                    'model_code': 'EV-NX1-PRO',
                    'price': 1499.99,
                    'specs': {
                        'sensor': '28.2MP APS-C BSI CMOS',
                        'lens_mount': 'Samsung NX-mount',
                        'iso_range': '100 - 51200',
                        'video': '4K UHD @ 30fps, 1080p @ 120fps',
                        'display': '3.0" Super AMOLED touchscreen',
                        'viewfinder': 'Electronic (2.36M dots)',
                        'autofocus': '205-point phase detection',
                        'burst_shooting': '15 fps',
                        'weather_sealing': 'Weather and dust resistant',
                        'connectivity': 'Wi-Fi, Bluetooth, NFC, HDMI',
                        'features': 'DRIMe V Image Processor, 4K video, Pro controls'
                    }
                }
            ]
        }
    ]

    # Camera Lenses
    lens_products = [
        {
            'name': 'Samsung NX 16-50mm f/2.0-2.8 S ED OIS Lens',
            'model_code': 'NX-16-50S',
            'category': lens_cat,
            'variants': [
                {
                    'name': 'Standard Zoom Lens',
                    'model_code': 'NX-16-50S-STD',
                    'price': 699.99,
                    'specs': {
                        'focal_length': '16-50mm (35mm equivalent: 24-75mm)',
                        'aperture': 'f/2.0 - f/2.8',
                        'construction': '18 elements in 12 groups',
                        'elements': '2 aspherical, 3 ED elements',
                        'filter_size': '72mm',
                        'closest_focus': '0.35m',
                        'image_stabilization': 'Optical Image Stabilization',
                        'autofocus': 'Voice Coil Motor (VCM)',
                        'features': 'Weather sealed, Premium build, Fast aperture'
                    }
                }
            ]
        },
        {
            'name': 'Samsung NX 30mm f/2.0 Pancake Lens',
            'model_code': 'NX-30MM',
            'category': lens_cat,
            'variants': [
                {
                    'name': 'Pancake Prime Lens',
                    'model_code': 'NX-30MM-PANCAKE',
                    'price': 249.99,
                    'specs': {
                        'focal_length': '30mm (35mm equivalent: 46mm)',
                        'aperture': 'f/2.0',
                        'construction': '7 elements in 5 groups',
                        'elements': '1 aspherical element',
                        'filter_size': '43mm',
                        'closest_focus': '0.35m',
                        'autofocus': 'Stepping Motor (STM)',
                        'features': 'Compact design, Fast aperture, Sharp optics'
                    }
                }
            ]
        },
        {
            'name': 'Samsung NX 85mm f/1.4 ED SSA Lens',
            'model_code': 'NX-85MM',
            'category': lens_cat,
            'variants': [
                {
                    'name': 'Portrait Prime Lens',
                    'model_code': 'NX-85MM-PORTRAIT',
                    'price': 899.99,
                    'specs': {
                        'focal_length': '85mm (35mm equivalent: 130mm)',
                        'aperture': 'f/1.4',
                        'construction': '9 elements in 7 groups',
                        'elements': '1 aspherical, 1 ED element',
                        'filter_size': '67mm',
                        'closest_focus': '0.8m',
                        'autofocus': 'Supersonic Actuator (SSA)',
                        'features': 'Beautiful bokeh, Portrait photography, Weather sealed'
                    }
                }
            ]
        },
        {
            'name': 'Samsung NX 50-150mm f/2.8 S ED OIS Lens',
            'model_code': 'NX-50-150S',
            'category': lens_cat,
            'variants': [
                {
                    'name': 'Telephoto Zoom Lens',
                    'model_code': 'NX-50-150S-TELE',
                    'price': 1299.99,
                    'specs': {
                        'focal_length': '50-150mm (35mm equivalent: 77-231mm)',
                        'aperture': 'f/2.8',
                        'construction': '20 elements in 16 groups',
                        'elements': '3 aspherical, 4 ED elements',
                        'filter_size': '72mm',
                        'closest_focus': '1.2m',
                        'image_stabilization': 'Optical Image Stabilization',
                        'autofocus': 'Voice Coil Motor (VCM)',
                        'features': 'Professional telephoto, Fast constant aperture, Weather sealed'
                    }
                }
            ]
        }
    ]

    # Camera Accessories
    accessory_products = [
        {
            'name': 'Samsung Camera Battery Grip',
            'model_code': 'BG-NX1',
            'category': accessories_cat,
            'variants': [
                {
                    'name': 'Vertical Battery Grip for NX1',
                    'model_code': 'BG-NX1-STD',
                    'price': 299.99,
                    'specs': {
                        'compatibility': 'Samsung NX1',
                        'battery_capacity': '2x BP1410 batteries',
                        'controls': 'Vertical shutter, dial, buttons',
                        'material': 'Magnesium alloy',
                        'weather_sealing': 'Weather resistant',
                        'weight': '280g (without batteries)',
                        'features': 'Extended shooting, Improved ergonomics, Vertical shooting'
                    }
                }
            ]
        },
        {
            'name': 'Samsung External Flash',
            'model_code': 'SEF-580',
            'category': accessories_cat,
            'variants': [
                {
                    'name': 'Dedicated Flash Unit',
                    'model_code': 'SEF-580-STD',
                    'price': 349.99,
                    'specs': {
                        'guide_number': '58 (m @ ISO 100)',
                        'zoom_range': '24-200mm',
                        'tilt_angle': '-7° to +90°',
                        'swivel_angle': '0° to 180°',
                        'recycle_time': '2.5 seconds',
                        'power_source': '4x AA batteries',
                        'wireless': 'Wireless TTL control',
                        'features': 'High-speed sync, Wireless master/slave, LCD display'
                    }
                }
            ]
        },
        {
            'name': 'Samsung Camera Remote Control',
            'model_code': 'ED-RR1',
            'category': accessories_cat,
            'variants': [
                {
                    'name': 'Wireless Remote Shutter',
                    'model_code': 'ED-RR1-WIRELESS',
                    'price': 79.99,
                    'specs': {
                        'range': 'Up to 15m',
                        'functions': 'Shutter release, 2s delay, Video start/stop',
                        'power_source': 'CR2032 battery',
                        'compatibility': 'Samsung NX series',
                        'features': 'Wireless operation, Compact design, Long battery life'
                    }
                }
            ]
        },
        {
            'name': 'Samsung Camera Case',
            'model_code': 'CC-NX1',
            'category': accessories_cat,
            'variants': [
                {
                    'name': 'Professional Camera Case',
                    'model_code': 'CC-NX1-PRO',
                    'price': 129.99,
                    'specs': {
                        'material': 'Nylon with leather accents',
                        'compatibility': 'NX1 with standard lens',
                        'protection': 'Padded interior, Weather resistant',
                        'carrying_options': 'Shoulder strap, Belt loop',
                        'pockets': 'Multiple accessory pockets',
                        'features': 'Professional protection, Quick access, Weather resistant'
                    }
                }
            ]
        }
    ]

    # Action Cameras
    action_cam_products = [
        {
            'name': 'Samsung Gear 360 Camera',
            'model_code': 'SM-R210',
            'category': action_cam_cat,
            'variants': [
                {
                    'name': '360° Action Camera',
                    'model_code': 'SM-R210-360',
                    'price': 349.99,
                    'specs': {
                        'resolution': '30.4MP total (15.2MP per lens)',
                        'video': '4K 360° video @ 24fps',
                        'lenses': 'Dual fisheye lenses',
                        'connectivity': 'Wi-Fi, Bluetooth, NFC',
                        'storage': 'microSD up to 256GB',
                        'battery': '1350mAh',
                        'water_resistance': 'IP53 (splash resistant)',
                        'features': '360° content creation, Live streaming, VR compatibility'
                    }
                }
            ]
        },
        {
            'name': 'Samsung Gear 360 (2017 Edition)',
            'model_code': 'SM-R210N',
            'category': action_cam_cat,
            'variants': [
                {
                    'name': 'Improved 360° Camera',
                    'model_code': 'SM-R210N-2017',
                    'price': 229.99,
                    'specs': {
                        'resolution': '15MP total (8.4MP per lens)',
                        'video': '4K 360° video @ 24fps',
                        'lenses': 'Dual fisheye lenses',
                        'connectivity': 'Wi-Fi, Bluetooth, NFC',
                        'storage': 'microSD up to 256GB',
                        'battery': '1350mAh',
                        'water_resistance': 'IP53 (splash resistant)',
                        'features': 'Improved low light, Better stitching, Compact design'
                    }
                }
            ]
        }
    ]

    all_products = camera_products + lens_products + accessory_products + action_cam_products

    with transaction.atomic():
        for product_data in all_products:
            # Check if product already exists
            existing_product = Product.objects.filter(slug=f"{product_data['model_code'].lower()}").first()
            
            if existing_product:
                print(f"⚠️  Product {product_data['name']} already exists, skipping...")
                continue
                
            product = Product.objects.create(
                name=product_data['name'],
                slug=f"{product_data['model_code'].lower()}",
                description=f"Professional {product_data['name']} with advanced imaging technology and superior optics",
                short_description=f"High-quality {product_data['name']} for photography enthusiasts and professionals",
                warranty_period=24,
                features=['Professional Quality', 'Advanced Technology', 'Smart Features', 'Warranty Support'],
                category=product_data['category'],
                is_featured=True if 'NX1' in product_data['name'] or '85mm' in product_data['name'] else False,
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

    print(f"🎉 Created {len(all_products)} Cameras & Imaging products!")
    print(f"📷 Total variants: {sum(len(p['variants']) for p in all_products)}")
    print(f"📸 Categories: Digital Cameras, Camera Lenses, Camera Accessories, Action Cameras")

if __name__ == "__main__":
    create_cameras_imaging()
