import setup_django

from django.db import transaction
from home.models import ProductCategory, Product, ProductVariant, ProductSpecification

def create_smart_home_iot():
    # SmartThings Devices category
    smartthings_cat, _ = ProductCategory.objects.get_or_create(name="SmartThings Devices", defaults={'slug': 'smartthings-devices'})

    # Smart Cameras
    camera_products = [
        {
            'name': 'Samsung SmartThings Cam',
            'model_code': 'ST-CAM-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'Indoor Smart Camera 1080p',
                    'model_code': 'ST-CAM-INDOOR',
                    'price': 89.99,
                    'specs': {
                        'resolution': '1080p Full HD',
                        'field_of_view': '130° diagonal',
                        'night_vision': 'Yes, up to 16ft',
                        'two_way_audio': 'Yes',
                        'motion_detection': 'Yes',
                        'person_detection': 'AI-powered',
                        'storage': 'Cloud + Local SD card',
                        'connectivity': 'Wi-Fi 2.4GHz',
                        'power': 'USB-C + Battery backup',
                        'features': 'SmartThings integration, Privacy mode, Activity zones'
                    }
                },
                {
                    'name': 'Outdoor Smart Camera 1080p',
                    'model_code': 'ST-CAM-OUTDOOR',
                    'price': 129.99,
                    'specs': {
                        'resolution': '1080p Full HD',
                        'field_of_view': '145° diagonal',
                        'night_vision': 'Yes, up to 25ft with IR',
                        'two_way_audio': 'Yes',
                        'motion_detection': 'Yes',
                        'person_detection': 'AI-powered',
                        'weather_resistance': 'IP65 weatherproof',
                        'storage': 'Cloud + Local SD card',
                        'connectivity': 'Wi-Fi 2.4GHz',
                        'power': 'AC adapter + Battery backup',
                        'features': 'SmartThings integration, Siren, Floodlight option'
                    }
                },
                {
                    'name': '4K Smart Camera Indoor',
                    'model_code': 'ST-CAM-4K',
                    'price': 179.99,
                    'specs': {
                        'resolution': '4K Ultra HD',
                        'field_of_view': '140° diagonal',
                        'night_vision': 'Color night vision up to 20ft',
                        'two_way_audio': 'Yes with noise cancellation',
                        'motion_detection': 'AI-powered with zones',
                        'person_detection': 'Advanced AI recognition',
                        'storage': 'Cloud + Local 256GB SD card',
                        'connectivity': 'Wi-Fi 5GHz',
                        'power': 'USB-C',
                        'features': 'SmartThings integration, 360° view, Privacy shutter'
                    }
                }
            ]
        },
        {
            'name': 'Samsung SmartThings Video Doorbell',
            'model_code': 'ST-DOORBELL-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'Video Doorbell Pro',
                    'model_code': 'ST-DOORBELL-PRO',
                    'price': 199.99,
                    'specs': {
                        'resolution': '1080p Full HD',
                        'field_of_view': '180° vertical',
                        'night_vision': 'Yes, color night vision',
                        'two_way_audio': 'Yes with noise reduction',
                        'motion_detection': 'Person detection',
                        'doorbell_chime': 'Digital chime options',
                        'power': 'Wired or Battery',
                        'storage': 'Cloud + Local',
                        'connectivity': 'Wi-Fi 2.4GHz',
                        'features': 'SmartThings integration, Package detection, Quick replies'
                    }
                }
            ]
        }
    ]

    # Smart Plugs & Sensors
    plug_sensor_products = [
        {
            'name': 'Samsung SmartThings Smart Plug',
            'model_code': 'ST-PLUG-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'Smart Plug Mini',
                    'model_code': 'ST-PLUG-MINI',
                    'price': 19.99,
                    'specs': {
                        'power_rating': '15A/1800W',
                        'wireless_protocol': 'Zigbee',
                        'connectivity': 'SmartThings Hub required',
                        'monitoring': 'Energy monitoring',
                        'schedule': 'Custom schedules',
                        'voice_control': 'Alexa, Google Assistant',
                        'features': 'Away mode, Random on/off, Compact design'
                    }
                },
                {
                    'name': 'Smart Plug Outdoor',
                    'model_code': 'ST-PLUG-OUTDOOR',
                    'price': 34.99,
                    'specs': {
                        'power_rating': '15A/1800W',
                        'wireless_protocol': 'Zigbee',
                        'connectivity': 'SmartThings Hub required',
                        'weather_resistance': 'IP44 weatherproof',
                        'monitoring': 'Energy monitoring',
                        'schedule': 'Custom schedules',
                        'features': 'Outdoor use, Holiday lighting control, Timer functions'
                    }
                },
                {
                    'name': 'Smart Power Strip',
                    'model_code': 'ST-STRIP-001',
                    'price': 49.99,
                    'specs': {
                        'outlets': '4 smart outlets + 2 USB-A',
                        'power_rating': '15A/1875W total',
                        'wireless_protocol': 'Zigbee',
                        'connectivity': 'SmartThings Hub required',
                        'monitoring': 'Per-outlet energy monitoring',
                        'control': 'Individual outlet control',
                        'features': 'USB charging, Surge protection, Each outlet controllable'
                    }
                }
            ]
        },
        {
            'name': 'Samsung SmartThings Motion Sensor',
            'model_code': 'ST-MOTION-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'Motion Sensor',
                    'model_code': 'ST-MOTION-STD',
                    'price': 29.99,
                    'specs': {
                        'detection_range': '15-20 feet',
                        'detection_angle': '120°',
                        'wireless_protocol': 'Zigbee',
                        'battery_life': 'Up to 2 years',
                        'connectivity': 'SmartThings Hub required',
                        'sensitivity': 'Adjustable sensitivity',
                        'features': 'Pet immune up to 40lbs, Temperature sensing, Compact design'
                    }
                }
            ]
        },
        {
            'name': 'Samsung SmartThings Multipurpose Sensor',
            'model_code': 'ST-MULTI-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'Multipurpose Sensor',
                    'model_code': 'ST-MULTI-STD',
                    'price': 24.99,
                    'specs': {
                        'functions': 'Open/close, vibration, temperature',
                        'wireless_protocol': 'Zigbee',
                        'battery_life': 'Up to 2 years',
                        'connectivity': 'SmartThings Hub required',
                        'magnet_range': '5mm gap detection',
                        'features': 'Door/window monitoring, Temperature alerts, Vibration detection'
                    }
                }
            ]
        },
        {
            'name': 'Samsung SmartThings Water Leak Sensor',
            'model_code': 'ST-WATER-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'Water Leak Sensor',
                    'model_code': 'ST-WATER-STD',
                    'price': 39.99,
                    'specs': {
                        'detection': 'Water presence detection',
                        'wireless_protocol': 'Zigbee',
                        'battery_life': 'Up to 2 years',
                        'connectivity': 'SmartThings Hub required',
                        'probe_length': '6ft detachable probe',
                        'features': 'Leak alerts, Temperature monitoring, Humidity sensing'
                    }
                }
            ]
        }
    ]

    # Smart Lighting
    lighting_products = [
        {
            'name': 'Samsung SmartThings Smart Bulb',
            'model_code': 'ST-BULB-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'A19 Smart LED Bulb',
                    'model_code': 'ST-BULB-A19',
                    'price': 14.99,
                    'specs': {
                        'brightness': '800 lumens',
                        'color_temperature': '2700K - 6500K',
                        'dimming': '10% - 100%',
                        'wireless_protocol': 'Zigbee',
                        'connectivity': 'SmartThings Hub required',
                        'lifespan': '25,000 hours',
                        'features': 'Tunable white, Schedules, Scenes, Energy efficient'
                    }
                },
                {
                    'name': 'BR30 Smart LED Bulb',
                    'model_code': 'ST-BULB-BR30',
                    'price': 16.99,
                    'specs': {
                        'brightness': '650 lumens',
                        'color_temperature': '2700K - 6500K',
                        'dimming': '10% - 100%',
                        'wireless_protocol': 'Zigbee',
                        'connectivity': 'SmartThings Hub required',
                        'lifespan': '25,000 hours',
                        'features': 'Tunable white, Floodlight, Schedules, Energy efficient'
                    }
                },
                {
                    'name': 'Color Smart LED Bulb',
                    'model_code': 'ST-BULB-COLOR',
                    'price': 24.99,
                    'specs': {
                        'brightness': '800 lumens',
                        'colors': '16 million colors',
                        'color_temperature': '2700K - 6500K',
                        'dimming': '10% - 100%',
                        'wireless_protocol': 'Zigbee',
                        'connectivity': 'SmartThings Hub required',
                        'lifespan': '25,000 hours',
                        'features': 'Full color control, Scenes, Music sync, Energy efficient'
                    }
                }
            ]
        },
        {
            'name': 'Samsung SmartThings Smart Light Switch',
            'model_code': 'ST-SWITCH-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'Smart Light Switch',
                    'model_code': 'ST-SWITCH-STD',
                    'price': 44.99,
                    'specs': {
                        'type': 'Single pole switch',
                        'wireless_protocol': 'Zigbee',
                        'connectivity': 'SmartThings Hub required',
                        'power': '120-277V AC',
                        'installation': 'Neutral wire required',
                        'features': 'Manual control, App control, Schedules, 3-way compatible'
                    }
                },
                {
                    'name': 'Smart Dimmer Switch',
                    'model_code': 'ST-DIMMER-STD',
                    'price': 54.99,
                    'specs': {
                        'type': 'Single pole dimmer',
                        'wireless_protocol': 'Zigbee',
                        'connectivity': 'SmartThings Hub required',
                        'power': '120-277V AC',
                        'dimming': '10% - 100%',
                        'installation': 'Neutral wire required',
                        'features': 'Dimming control, App control, Schedules, 3-way compatible'
                    }
                }
            ]
        },
        {
            'name': 'Samsung SmartThings Smart Plug',
            'model_code': 'ST-PLUG-LIGHT-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'Smart Plug for Lamps',
                    'model_code': 'ST-PLUG-LAMP',
                    'price': 22.99,
                    'specs': {
                        'power_rating': '10A/1200W',
                        'wireless_protocol': 'Zigbee',
                        'connectivity': 'SmartThings Hub required',
                        'monitoring': 'Energy monitoring',
                        'schedule': 'Custom schedules',
                        'features': 'Lamp control, Dimming compatible, Away mode'
                    }
                }
            ]
        }
    ]

    # Smart Home Integration
    integration_products = [
        {
            'name': 'Samsung SmartThings Hub',
            'model_code': 'ST-HUB-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'SmartThings Hub 3rd Gen',
                    'model_code': 'ST-HUB-3RD',
                    'price': 99.99,
                    'specs': {
                        'protocols': 'Zigbee, Z-Wave, Bluetooth, Wi-Fi',
                        'connectivity': 'Ethernet, Wi-Fi',
                        'device_capacity': 'Up to 200 devices',
                        'range': 'Zigbee: 130ft, Z-Wave: 130ft',
                        'backup_power': 'Battery backup (4 hours)',
                        'features': 'Local processing, Cloud backup, Alexa/Google integration, IFTTT'
                    }
                }
            ]
        },
        {
            'name': 'Samsung SmartThings Station',
            'model_code': 'ST-STATION-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'SmartThings Station',
                    'model_code': 'ST-STATION-STD',
                    'price': 149.99,
                    'specs': {
                        'protocols': 'Zigbee, Thread, Matter, Wi-Fi',
                        'connectivity': 'Wi-Fi 6, Bluetooth 5.0',
                        'device_capacity': 'Up to 250 devices',
                        'display': '1.2" LCD screen',
                        'speaker': 'Built-in speaker',
                        'microphone': 'Far-field voice recognition',
                        'features': 'Matter support, Thread border router, Voice assistant, Local processing'
                    }
                }
            ]
        },
        {
            'name': 'Samsung SmartThings Smart Display',
            'model_code': 'ST-DISPLAY-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'Smart Display 7"',
                    'model_code': 'ST-DISPLAY-7',
                    'price': 199.99,
                    'specs': {
                        'display': '7" touchscreen LCD',
                        'resolution': '1024 x 600',
                        'protocols': 'Zigbee, Thread, Matter, Wi-Fi',
                        'connectivity': 'Wi-Fi 6, Bluetooth 5.0',
                        'speaker': '2x 5W speakers',
                        'microphone': 'Far-field voice recognition',
                        'camera': '5MP privacy camera',
                        'features': 'Control center, Video calls, Smart home dashboard, Matter support'
                    }
                }
            ]
        },
        {
            'name': 'Samsung SmartThings Smart Thermostat',
            'model_code': 'ST-THERMO-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'Smart Thermostat',
                    'model_code': 'ST-THERMO-STD',
                    'price': 179.99,
                    'specs': {
                        'display': '3.5" color touchscreen',
                        'compatibility': 'Most HVAC systems',
                        'protocols': 'Zigbee, Wi-Fi',
                        'connectivity': 'Wi-Fi 2.4GHz',
                        'power': 'C-wire required',
                        'learning': 'AI-powered learning',
                        'features': 'Geofencing, Energy reports, Voice control, Schedules'
                    }
                }
            ]
        },
        {
            'name': 'Samsung SmartThings Smart Lock',
            'model_code': 'ST-LOCK-001',
            'category': smartthings_cat,
            'variants': [
                {
                    'name': 'Smart Door Lock',
                    'model_code': 'ST-LOCK-STD',
                    'price': 229.99,
                    'specs': {
                        'lock_type': 'Deadbolt',
                        'access_methods': 'Keypad, App, Auto-lock',
                        'protocols': 'Zigbee, BLE',
                        'connectivity': 'SmartThings Hub required',
                        'power': '4x AA batteries',
                        'battery_life': '6-12 months',
                        'features': 'Guest codes, Activity log, Auto-lock, Tamper alerts'
                    }
                }
            ]
        }
    ]

    all_products = camera_products + plug_sensor_products + lighting_products + integration_products

    with transaction.atomic():
        for product_data in all_products:
            product = Product.objects.create(
                name=product_data['name'],
                slug=f"{product_data['model_code'].lower()}",
                description=f"Advanced {product_data['name']} with SmartThings integration and cutting-edge IoT technology",
                short_description=f"Premium {product_data['name']} for complete smart home automation",
                warranty_period=24,
                features=['SmartThings Integration', 'Voice Control', 'Energy Efficient', 'Mobile App Control'],
                category=product_data['category'],
                is_featured=True if 'Hub' in product_data['name'] or 'Station' in product_data['name'] else False,
                is_active=True
            )
            
            for variant_data in product_data['variants']:
                variant = ProductVariant.objects.create(
                    product=product,
                    name=variant_data['name'],
                    model_code=variant_data['model_code'],
                    price=variant_data['price'],
                    stock_quantity=50,
                    min_stock_level=10,
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

    print(f"🎉 Created {len(all_products)} Smart Home & IoT products!")
    print(f"🏠 Total variants: {sum(len(p['variants']) for p in all_products)}")
    print(f"📱 Categories: Smart Cameras, Smart Plugs & Sensors, Smart Lighting, Smart Home Integration")

if __name__ == "__main__":
    create_smart_home_iot()
