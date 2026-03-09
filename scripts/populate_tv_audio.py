import setup_django

from django.db import transaction
from home.models import ProductCategory, Product, ProductVariant, ProductImage, ProductSpecification

def create_tv_audio_products():
    """Create comprehensive TV & Audio products with all variations"""
    
    # Get or create categories
    tv_category, _ = ProductCategory.objects.get_or_create(
        name="Televisions",
        defaults={'slug': 'televisions'}
    )
    
    audio_category, _ = ProductCategory.objects.get_or_create(
        name="Home Audio", 
        defaults={'slug': 'home-audio'}
    )
    
    accessories_category, _ = ProductCategory.objects.get_or_create(
        name="TV Accessories",
        defaults={'slug': 'tv-accessories'}
    )
    
    # TV Products Data
    tv_products = [
        {
            'name': 'Samsung QLED 4K Smart TV',
            'short_description': 'Premium 4K QLED TV with smart features',
            'description': 'Experience stunning picture quality with Samsung\'s revolutionary QLED technology. This 4K Smart TV delivers vibrant colors, deep blacks, and brilliant highlights. With built-in smart features, voice control, and multiple streaming apps, it\'s your complete entertainment hub.',
            'model_code': 'QN55Q80C',
            'warranty_period': 24,
            'features': [
                'Quantum HDR+',
                'Object Tracking Sound Lite',
                'Adaptive Picture',
                'Multi View',
                'Smart TV with Tizen OS',
                'Voice Remote',
                '4K AI Upscaling',
                'Game Mode',
                'Ambient Mode'
            ],
            'category': tv_category,
            'variants': [
                {
                    'name': '55-inch QLED',
                    'model_code': 'QN55Q80C-55',
                    'price': 1299.99,
                    'sale_price': 1099.99,
                    'cost_price': 950.00,
                    'stock_quantity': 25,
                    'min_stock_level': 5,
                    'availability': 'in_stock',
                    'specifications': {
                        'screen_size': '55-inch',
                        'resolution': '4K (3840x2160)',
                        'display_type': 'QLED',
                        'refresh_rate': '120Hz',
                        'hdmi_ports': '4',
                        'usb_ports': '2',
                        'smart_platform': 'Tizen OS',
                        'voice_control': 'Yes'
                    }
                },
                {
                    'name': '65-inch QLED',
                    'model_code': 'QN65Q80C-65',
                    'price': 1799.99,
                    'sale_price': 1499.99,
                    'cost_price': 1350.00,
                    'stock_quantity': 15,
                    'min_stock_level': 3,
                    'availability': 'in_stock',
                    'specifications': {
                        'screen_size': '65-inch',
                        'resolution': '4K (3840x2160)',
                        'display_type': 'QLED',
                        'refresh_rate': '120Hz',
                        'hdmi_ports': '4',
                        'usb_ports': '2',
                        'smart_platform': 'Tizen OS',
                        'voice_control': 'Yes'
                    }
                },
                {
                    'name': '75-inch QLED',
                    'model_code': 'QN75Q80C-75',
                    'price': 2499.99,
                    'sale_price': 2099.99,
                    'cost_price': 1900.00,
                    'stock_quantity': 8,
                    'min_stock_level': 2,
                    'availability': 'in_stock',
                    'specifications': {
                        'screen_size': '75-inch',
                        'resolution': '4K (3840x2160)',
                        'display_type': 'QLED',
                        'refresh_rate': '120Hz',
                        'hdmi_ports': '4',
                        'usb_ports': '2',
                        'smart_platform': 'Tizen OS',
                        'voice_control': 'Yes'
                    }
                }
            ]
        },
        {
            'name': 'Samsung Crystal UHD Smart TV',
            'short_description': 'Crystal clear 4K UHD Smart TV',
            'description': 'Enjoy crystal-clear visuals with Samsung\'s Crystal UHD technology. This Smart TV offers brilliant 4K resolution, smart features, and an intuitive interface that makes it easy to access your favorite content.',
            'model_code': 'UN50NU8000',
            'warranty_period': 24,
            'features': [
                'Crystal Processor 4K',
                'Crystal Display',
                'Smart TV with Tizen OS',
                'HDR10+',
                'HGiG',
                'Auto Low Latency Mode',
                'Adaptive Sound',
                'Multiple Voice Assistants'
            ],
            'category': tv_category,
            'variants': [
                {
                    'name': '50-inch Crystal UHD',
                    'model_code': 'UN50NU8000-50',
                    'price': 699.99,
                    'sale_price': 599.99,
                    'cost_price': 450.00,
                    'stock_quantity': 30,
                    'min_stock_level': 8,
                    'availability': 'in_stock',
                    'specifications': {
                        'screen_size': '50-inch',
                        'resolution': '4K (3840x2160)',
                        'display_type': 'Crystal UHD',
                        'refresh_rate': '60Hz',
                        'hdmi_ports': '3',
                        'usb_ports': '1',
                        'smart_platform': 'Tizen OS',
                        'voice_control': 'Yes'
                    }
                },
                {
                    'name': '55-inch Crystal UHD',
                    'model_code': 'UN55NU8000-55',
                    'price': 899.99,
                    'sale_price': 749.99,
                    'cost_price': 600.00,
                    'stock_quantity': 20,
                    'min_stock_level': 5,
                    'availability': 'in_stock',
                    'specifications': {
                        'screen_size': '55-inch',
                        'resolution': '4K (3840x2160)',
                        'display_type': 'Crystal UHD',
                        'refresh_rate': '60Hz',
                        'hdmi_ports': '3',
                        'usb_ports': '1',
                        'smart_platform': 'Tizen OS',
                        'voice_control': 'Yes'
                    }
                },
                {
                    'name': '65-inch Crystal UHD',
                    'model_code': 'UN65NU8000-65',
                    'price': 1199.99,
                    'sale_price': 999.99,
                    'cost_price': 850.00,
                    'stock_quantity': 12,
                    'min_stock_level': 3,
                    'availability': 'in_stock',
                    'specifications': {
                        'screen_size': '65-inch',
                        'resolution': '4K (3840x2160)',
                        'display_type': 'Crystal UHD',
                        'refresh_rate': '60Hz',
                        'hdmi_ports': '3',
                        'usb_ports': '1',
                        'smart_platform': 'Tizen OS',
                        'voice_control': 'Yes'
                    }
                }
            ]
        },
        {
            'name': 'Samsung Neo QLED 8K Smart TV',
            'short_description': 'Next-generation 8K Neo QLED TV',
            'description': 'Step into the future with Samsung\'s Neo QLED 8K TV. Featuring revolutionary Neo Quantum Processor, this TV delivers unprecedented brightness, contrast, and detail. Perfect for home theater enthusiasts who demand the best.',
            'model_code': 'QN900A',
            'warranty_period': 24,
            'features': [
                'Neo Quantum Processor 8K',
                'Infinity Screen',
                'Neo QLED Technology',
                '8K Resolution',
                'Quantum HDR 48+',
                'Object Tracking Sound Pro',
                'EyeComfort Mode',
                'Calman Mode',
                'Gaming Hub'
            ],
            'category': tv_category,
            'variants': [
                {
                    'name': '75-inch Neo QLED 8K',
                    'model_code': 'QN900A-75',
                    'price': 4999.99,
                    'sale_price': 4499.99,
                    'cost_price': 3800.00,
                    'stock_quantity': 5,
                    'min_stock_level': 2,
                    'availability': 'in_stock',
                    'specifications': {
                        'screen_size': '75-inch',
                        'resolution': '8K (7680x4320)',
                        'display_type': 'Neo QLED',
                        'refresh_rate': '144Hz',
                        'hdmi_ports': '4',
                        'usb_ports': '2',
                        'smart_platform': 'Tizen OS',
                        'voice_control': 'Yes',
                        'hdmi_2_1': 'Yes'
                    }
                },
                {
                    'name': '85-inch Neo QLED 8K',
                    'model_code': 'QN900A-85',
                    'price': 6999.99,
                    'sale_price': 6299.99,
                    'cost_price': 5500.00,
                    'stock_quantity': 3,
                    'min_stock_level': 1,
                    'availability': 'in_stock',
                    'specifications': {
                        'screen_size': '85-inch',
                        'resolution': '8K (7680x4320)',
                        'display_type': 'Neo QLED',
                        'refresh_rate': '144Hz',
                        'hdmi_ports': '4',
                        'usb_ports': '2',
                        'smart_platform': 'Tizen OS',
                        'voice_control': 'Yes',
                        'hdmi_2_1': 'Yes'
                    }
                }
            ]
        },
        {
            'name': 'Samsung Lifestyle TV The Frame',
            'short_description': 'Art-like TV that transforms your space',
            'description': 'The Frame transforms from TV to beautiful art when not in use. With customizable bezels and art mode, it displays your favorite photos or artwork with stunning realism.',
            'model_code': 'LS03B',
            'warranty_period': 24,
            'features': [
                'Art Mode',
                'Customizable Bezels',
                'Slim Fit Wall Mount',
                'Motion Sensor',
                'SmartThings Integration',
                'Anti-Reflection Matte Display',
                'QLED 4K Display',
                'Multi-View Support'
            ],
            'category': tv_category,
            'variants': [
                {
                    'name': '55-inch The Frame',
                    'model_code': 'LS03B-55',
                    'price': 1599.99,
                    'sale_price': 1399.99,
                    'cost_price': 1200.00,
                    'stock_quantity': 18,
                    'min_stock_level': 4,
                    'availability': 'in_stock',
                    'specifications': {
                        'screen_size': '55-inch',
                        'resolution': '4K (3840x2160)',
                        'display_type': 'QLED',
                        'refresh_rate': '120Hz',
                        'art_mode': 'Yes',
                        'custom_bezels': 'Yes',
                        'motion_sensor': 'Yes'
                    }
                },
                {
                    'name': '65-inch The Frame',
                    'model_code': 'LS03B-65',
                    'price': 2199.99,
                    'sale_price': 1899.99,
                    'cost_price': 1650.00,
                    'stock_quantity': 10,
                    'min_stock_level': 2,
                    'availability': 'in_stock',
                    'specifications': {
                        'screen_size': '65-inch',
                        'resolution': '4K (3840x2160)',
                        'display_type': 'QLED',
                        'refresh_rate': '120Hz',
                        'art_mode': 'Yes',
                        'custom_bezels': 'Yes',
                        'motion_sensor': 'Yes'
                    }
                }
            ]
        }
    ]
    
    # Home Audio Products Data
    audio_products = [
        {
            'name': 'Samsung HW-Q990C Soundbar',
            'short_description': 'Premium wireless soundbar with Dolby Atmos',
            'description': 'Elevate your home audio experience with the Samsung HW-Q990C soundbar. Featuring Dolby Atmos support, wireless connectivity, and powerful bass, this soundbar delivers immersive cinema-quality sound.',
            'model_code': 'HW-Q990C',
            'warranty_period': 24,
            'features': [
                'Dolby Atmos',
                'DTS:X',
                'Wireless Subwoofer',
                'Adaptive Sound',
                'Q-Symphony',
                'Game Mode Pro',
                'Tap Sound',
                'Voice Control',
                'Multi-Connection Bluetooth'
            ],
            'category': audio_category,
            'variants': [
                {
                    'name': 'Standard Soundbar',
                    'model_code': 'HW-Q990C-STD',
                    'price': 899.99,
                    'sale_price': 799.99,
                    'cost_price': 650.00,
                    'stock_quantity': 25,
                    'min_stock_level': 8,
                    'availability': 'in_stock',
                    'specifications': {
                        'channels': '5.1.2',
                        'power_output': '550W',
                        'connectivity': 'Bluetooth 5.0',
                        'wireless_subwoofer': 'Included',
                        'dolby_atmos': 'Yes'
                    }
                },
                {
                    'name': 'Soundbar with Subwoofer Kit',
                    'model_code': 'HW-Q990C-KIT',
                    'price': 1299.99,
                    'sale_price': 1099.99,
                    'cost_price': 950.00,
                    'stock_quantity': 15,
                    'min_stock_level': 4,
                    'availability': 'in_stock',
                    'specifications': {
                        'channels': '5.1.2',
                        'power_output': '620W',
                        'connectivity': 'Bluetooth 5.0',
                        'wireless_subwoofer': 'Yes',
                        'dolby_atmos': 'Yes',
                        'subwoofer_power': '200W'
                    }
                }
            ]
        },
        {
            'name': 'Samsung HW-S800D Wireless Speakers',
            'short_description': 'Premium wireless speakers with room-filling sound',
            'description': 'Experience room-filling audio with Samsung HW-S800D wireless speakers. These sleek speakers deliver clear highs and rich bass, perfect for music lovers and home theater enthusiasts.',
            'model_code': 'HW-S800D',
            'warranty_period': 24,
            'features': [
                '360 Degree Sound',
                'Tap Sound',
                'Multi-Connection',
                'Room Correction',
                'Voice Control',
                'Adaptive Sound',
                'Wireless Charging Pad',
                'Multi-Room Audio'
            ],
            'category': audio_category,
            'variants': [
                {
                    'name': 'Single Speaker',
                    'model_code': 'HW-S800D-SINGLE',
                    'price': 249.99,
                    'sale_price': 199.99,
                    'cost_price': 180.00,
                    'stock_quantity': 40,
                    'min_stock_level': 10,
                    'availability': 'in_stock',
                    'specifications': {
                        'power_output': '120W',
                        'connectivity': 'Bluetooth 5.0',
                        'frequency_response': '60Hz-20kHz',
                        '360_sound': 'Yes',
                        'tap_sound': 'Yes'
                    }
                },
                {
                    'name': 'Speaker Pair',
                    'model_code': 'HW-S800D-PAIR',
                    'price': 449.99,
                    'sale_price': 399.99,
                    'cost_price': 320.00,
                    'stock_quantity': 20,
                    'min_stock_level': 5,
                    'availability': 'in_stock',
                    'specifications': {
                        'power_output': '240W total',
                        'connectivity': 'Bluetooth 5.0',
                        'frequency_response': '60Hz-20kHz',
                        '360_sound': 'Yes',
                        'tap_sound': 'Yes',
                        'stereo_pairing': 'Yes'
                    }
                }
            ]
        }
    ]
    
    # TV Accessories Products Data
    accessories_products = [
        {
            'name': 'Samsung Premium TV Mount',
            'short_description': 'Ultra-slim wall mount for Samsung TVs',
            'description': 'Secure your Samsung TV with this premium wall mount. Features ultra-slim design, easy installation, and built-in cable management for a clean, professional look.',
            'model_code': 'WMN-M55',
            'warranty_period': 12,
            'features': [
                'Ultra-Slim Design',
                'Built-in Cable Management',
                'Easy Installation',
                'Heavy-Duty Construction',
                'Tilt and Swivel',
                'Universal Compatibility',
                'Safety Tested'
            ],
            'category': accessories_category,
            'variants': [
                {
                    'name': 'Mount for 55-65 inch TVs',
                    'model_code': 'WMN-M55-STANDARD',
                    'price': 149.99,
                    'sale_price': 119.99,
                    'cost_price': 80.00,
                    'stock_quantity': 50,
                    'min_stock_level': 15,
                    'availability': 'in_stock',
                    'specifications': {
                        'tv_size_range': '55-65 inch',
                        'weight_capacity': '50kg',
                        'tilt_angle': '±15 degrees',
                        'vESA_compliance': 'Yes',
                        'material': 'Steel'
                    }
                },
                {
                    'name': 'Mount for 75-85 inch TVs',
                    'model_code': 'WMN-M55-LARGE',
                    'price': 199.99,
                    'sale_price': 169.99,
                    'cost_price': 120.00,
                    'stock_quantity': 30,
                    'min_stock_level': 8,
                    'availability': 'in_stock',
                    'specifications': {
                        'tv_size_range': '75-85 inch',
                        'weight_capacity': '75kg',
                        'tilt_angle': '±15 degrees',
                        'vESA_compliance': 'Yes',
                        'material': 'Steel'
                    }
                }
            ]
        },
        {
            'name': 'Samsung Smart Remote Control',
            'short_description': 'Advanced universal remote with voice control',
            'description': 'Control your entire entertainment system with this advanced smart remote. Features voice control, backlit buttons, and universal compatibility with all major brands.',
            'model_code': 'TM-2050',
            'warranty_period': 12,
            'features': [
                'Voice Control',
                'Backlit Display',
                'Universal Compatibility',
                'Quick Access Buttons',
                'Rechargeable Battery',
                'SmartThings App Control',
                'Motion Control',
                'Learning Function'
            ],
            'category': accessories_category,
            'variants': [
                {
                    'name': 'Standard Smart Remote',
                    'model_code': 'TM-2050-STD',
                    'price': 79.99,
                    'sale_price': 69.99,
                    'cost_price': 45.00,
                    'stock_quantity': 100,
                    'min_stock_level': 20,
                    'availability': 'in_stock',
                    'specifications': {
                        'battery_type': 'Rechargeable Li-ion',
                        'battery_life': '6 months',
                        'voice_control': 'Yes',
                        'backlight': 'LED',
                        'compatibility': 'Universal'
                    }
                },
                {
                    'name': 'Premium Smart Remote',
                    'model_code': 'TM-2050-PREM',
                    'price': 129.99,
                    'sale_price': 109.99,
                    'cost_price': 75.00,
                    'stock_quantity': 60,
                    'min_stock_level': 12,
                    'availability': 'in_stock',
                    'specifications': {
                        'battery_type': 'Rechargeable Li-ion',
                        'battery_life': '8 months',
                        'voice_control': 'Yes',
                        'backlight': 'OLED',
                        'compatibility': 'Universal',
                        'premium_material': 'Aluminum'
                    }
                }
            ]
        }
    ]
    
    # Combine all products
    all_products = tv_products + audio_products + accessories_products
    
    with transaction.atomic():
        for product_data in all_products:
            print(f"Creating product: {product_data['name']}")
            
            # Create product
            product = Product.objects.create(
                name=product_data['name'],
                slug=f"{product_data['model_code'].lower()}",
                description=product_data['description'],
                short_description=product_data['short_description'],
                warranty_period=product_data['warranty_period'],
                features=product_data['features'],
                category=product_data['category'],
                is_featured=True if 'QLED' in product_data['name'] or 'Neo' in product_data['name'] else False,
                is_active=True
            )
            
            # Create variants
            for variant_data in product_data['variants']:
                variant = ProductVariant.objects.create(
                    product=product,
                    name=variant_data['name'],
                    model_code=variant_data['model_code'],
                    price=variant_data['price'],
                    sale_price=variant_data.get('sale_price'),
                    cost_price=variant_data.get('cost_price'),
                    stock_quantity=variant_data['stock_quantity'],
                    min_stock_level=variant_data['min_stock_level'],
                    availability=variant_data['availability'],
                    specifications=variant_data['specifications'],
                    is_active=True
                )
                
                # Create specifications for the variant
                spec_display_order = 0
                for spec_category, spec_value in variant_data['specifications'].items():
                    ProductSpecification.objects.create(
                        product=product,
                        category=spec_category,
                        name=spec_category,
                        value=spec_value,
                        display_order=spec_display_order
                    )
                    spec_display_order += 1
            
            print(f"✅ Created {len(product_data['variants'])} variants for {product_data['name']}")
    
    print(f"\n🎉 Successfully created {len(all_products)} product categories!")
    print(f"📺 Total products created: {sum(len(p['variants']) for p in all_products)}")
    print(f"📊 Total variants created: {sum(len(p['variants']) for p in all_products)}")

if __name__ == "__main__":
    create_tv_audio_products()
