import os
import sys
import django

# Setup Django environment (reuse pattern from populate_categories.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Samsung.settings")
django.setup()

from django.db import transaction  # noqa: E402
from home.models import (  # noqa: E402
    ProductCategory,
    Product,
    ProductVariant,
    ProductSpecification,
)


# Minimal category metadata so this script can create missing nodes
_CATEGORY_META = {
    "mobile-wearables": {"name": "Mobile & Wearables", "parent": None},
    "smartphones": {"name": "Smartphones", "parent": "mobile-wearables"},
    "galaxy-s-series": {"name": "Galaxy S Series", "parent": "smartphones"},
    "galaxy-note-series": {"name": "Galaxy Note Series", "parent": "smartphones"},
    "galaxy-z-series": {"name": "Galaxy Z Series", "parent": "smartphones"},
    "galaxy-a-series": {"name": "Galaxy A Series", "parent": "smartphones"},
    "tablets": {"name": "Tablets", "parent": "mobile-wearables"},
    "galaxy-tab-s-series": {"name": "Galaxy Tab S Series", "parent": "tablets"},
    "galaxy-tab-a-series": {"name": "Galaxy Tab A Series", "parent": "tablets"},
    "smartwatches-wearables": {"name": "Smartwatches & Wearables", "parent": "mobile-wearables"},
    "galaxy-watch-series": {"name": "Galaxy Watch Series", "parent": "smartwatches-wearables"},
    "galaxy-fit-bands": {"name": "Galaxy Fit & Bands", "parent": "smartwatches-wearables"},
    "mobile-accessories": {"name": "Mobile Accessories", "parent": "mobile-wearables"},
    "phone-cases-covers": {"name": "Phone cases & covers", "parent": "mobile-accessories"},
    "chargers-cables": {"name": "Chargers & cables", "parent": "mobile-accessories"},
    "earbuds-galaxy-buds": {"name": "Earbuds (Galaxy Buds)", "parent": "mobile-accessories"},
}


def get_or_create_category(slug: str) -> ProductCategory:
    """
    Robust category lookup that:
    - Returns existing category by slug when present
    - Creates missing categories using a minimal tree that matches scripts/populate_categories.py
    """
    try:
        return ProductCategory.objects.get(slug=slug)
    except ProductCategory.DoesNotExist:
        meta = _CATEGORY_META.get(slug)
        if not meta:
            # If we don't know how to build this slug, surface the original error
            raise
        parent = get_or_create_category(meta["parent"]) if meta["parent"] else None
        category, _ = ProductCategory.objects.get_or_create(
            slug=slug,
            defaults={
                "name": meta["name"],
                "parent": parent,
            },
        )
        return category


def seed_mobile_and_wearables():
    """
    Populate a rich Samsung Mobile & Wearables catalog:
    - Smartphones (Galaxy S / Z / A / Note)
    - Tablets (Galaxy Tab S / A)
    - Smartwatches & bands (Galaxy Watch / Fit)
    - Core mobile accessories (Buds, chargers, cases)

    NOTE: This is a curated but non‑exhaustive catalog focused on
    current and iconic lines, not every single global SKU.
    """

    # Ensure category tree exists (create missing nodes if needed)
    mobile_root = get_or_create_category("mobile-wearables")
    smartphones = get_or_create_category("smartphones")
    galaxy_s = get_or_create_category("galaxy-s-series")
    galaxy_note = get_or_create_category("galaxy-note-series")
    galaxy_z = get_or_create_category("galaxy-z-series")
    galaxy_a = get_or_create_category("galaxy-a-series")

    tablets = get_or_create_category("tablets")
    tab_s = get_or_create_category("galaxy-tab-s-series")
    tab_a = get_or_create_category("galaxy-tab-a-series")

    wearables = get_or_create_category("smartwatches-wearables")
    watch_series = get_or_create_category("galaxy-watch-series")
    fit_bands = get_or_create_category("galaxy-fit-bands")

    mobile_accessories = get_or_create_category("mobile-accessories")
    phone_cases = get_or_create_category("phone-cases-covers")
    chargers_cables = get_or_create_category("chargers-cables")
    earbuds_cat = get_or_create_category("earbuds-galaxy-buds")

    products_data = [
        # ───────── Smartphones – Galaxy S ─────────
        {
            "name": "Samsung Galaxy S24 Ultra",
            "slug": "samsung-galaxy-s24-ultra",
            "category": galaxy_s,
            "short_description": "Ultimate Galaxy flagship with S Pen, AI and pro camera.",
            "description": (
                "Samsung Galaxy S24 Ultra combines a titanium frame, integrated S Pen, "
                "and Galaxy AI features with a 200MP quad camera system and a large Dynamic AMOLED 2X display."
            ),
            "features": [
                "6.8\" QHD+ Dynamic AMOLED 2X, 1–120Hz",
                "Snapdragon 8 Gen 3 for Galaxy",
                "200MP quad rear camera with 5x optical zoom",
                "12MP front camera with Nightography",
                "S Pen with low‑latency in‑screen writing",
                "5000mAh battery with Super Fast Charging",
                "IP68 water and dust resistance",
                "Galaxy AI features including Live Translate and Note Assist",
            ],
            "is_featured": True,
            "variants": [
                {
                    "name": "256GB / 12GB – Titanium Black",
                    "model_code": "SM-S928B-256-TBK",
                    "price": 189999,
                    "sale_price": 179999,
                    "stock_quantity": 20,
                    "specs": [
                        ("Display", "Screen Size", '6.8"'),
                        ("Display", "Panel", "Dynamic AMOLED 2X, 120Hz"),
                        ("Camera", "Rear Camera", "200MP + 50MP + 12MP + 10MP"),
                        ("Camera", "Front Camera", "12MP"),
                        ("Performance", "Processor", "Snapdragon 8 Gen 3 for Galaxy"),
                        ("Memory", "RAM", "12GB"),
                        ("Memory", "Storage", "256GB"),
                        ("Battery", "Capacity", "5000mAh"),
                    ],
                },
                {
                    "name": "512GB / 12GB – Titanium Gray",
                    "model_code": "SM-S928B-512-TGR",
                    "price": 204999,
                    "sale_price": 194999,
                    "stock_quantity": 15,
                    "specs": [
                        ("Memory", "Storage", "512GB"),
                    ],
                },
                {
                    "name": "1TB / 12GB – Titanium Violet",
                    "model_code": "SM-S928B-1TB-TVIO",
                    "price": 224999,
                    "sale_price": None,
                    "stock_quantity": 8,
                    "specs": [
                        ("Memory", "Storage", "1TB"),
                    ],
                },
            ],
        },
        {
            "name": "Samsung Galaxy S24+",
            "slug": "samsung-galaxy-s24-plus",
            "category": galaxy_s,
            "short_description": "Large screen flagship with Galaxy AI and long battery.",
            "description": (
                "Galaxy S24+ offers a 6.7‑inch Dynamic AMOLED 2X display, powerful camera system, "
                "and Galaxy AI features in a refined flat‑edge design."
            ),
            "features": [
                "6.7\" QHD+ Dynamic AMOLED 2X, 120Hz",
                "Galaxy AI features",
                "50MP triple rear camera with 3x optical zoom",
                "4900mAh battery with Super Fast Charging",
                "IP68 water and dust resistance",
            ],
            "variants": [
                {
                    "name": "256GB / 12GB – Onyx Black",
                    "model_code": "SM-S926B-256-BLK",
                    "price": 149999,
                    "sale_price": 144999,
                    "stock_quantity": 25,
                    "specs": [],
                },
                {
                    "name": "512GB / 12GB – Marble Gray",
                    "model_code": "SM-S926B-512-GRY",
                    "price": 164999,
                    "sale_price": None,
                    "stock_quantity": 10,
                    "specs": [],
                },
            ],
        },
        {
            "name": "Samsung Galaxy S24",
            "slug": "samsung-galaxy-s24",
            "category": galaxy_s,
            "short_description": "Compact Galaxy flagship with AI features.",
            "description": (
                "Galaxy S24 packs flagship power and Galaxy AI into a compact 6.2‑inch design, "
                "with a bright AMOLED display and versatile triple camera."
            ),
            "features": [
                "6.2\" FHD+ Dynamic AMOLED 2X, 120Hz",
                "Galaxy AI features such as Circle to Search",
                "50MP triple rear camera",
                "4000mAh battery",
                "IP68 water and dust resistance",
            ],
            "variants": [
                {
                    "name": "128GB / 8GB – Cobalt Violet",
                    "model_code": "SM-S921B-128-VIO",
                    "price": 119999,
                    "sale_price": 114999,
                    "stock_quantity": 30,
                    "specs": [],
                },
                {
                    "name": "256GB / 8GB – Onyx Black",
                    "model_code": "SM-S921B-256-BLK",
                    "price": 129999,
                    "sale_price": None,
                    "stock_quantity": 20,
                    "specs": [],
                },
            ],
        },
        # ───────── Smartphones – Galaxy Z ─────────
        {
            "name": "Samsung Galaxy Z Fold5",
            "slug": "samsung-galaxy-z-fold-5",
            "category": galaxy_z,
            "short_description": "Foldable productivity flagship with large inner display.",
            "description": (
                "Galaxy Z Fold5 unfolds into a tablet‑like 7.6‑inch screen with S Pen support, "
                "ideal for multitasking, productivity and immersive entertainment."
            ),
            "features": [
                "7.6\" inner + 6.2\" cover Dynamic AMOLED 2X displays",
                "Snapdragon 8 Gen 2 for Galaxy",
                "S Pen Fold Edition support",
                "Triple rear camera with 3x telephoto",
                "4400mAh dual battery",
                "IPX8 water resistance",
            ],
            "variants": [
                {
                    "name": "256GB / 12GB",
                    "model_code": "SM-F946B-256",
                    "price": 239999,
                    "sale_price": None,
                    "stock_quantity": 10,
                    "specs": [],
                },
                {
                    "name": "512GB / 12GB",
                    "model_code": "SM-F946B-512",
                    "price": 259999,
                    "sale_price": None,
                    "stock_quantity": 8,
                    "specs": [],
                },
                {
                    "name": "1TB / 12GB",
                    "model_code": "SM-F946B-1TB",
                    "price": 289999,
                    "sale_price": None,
                    "stock_quantity": 5,
                    "specs": [],
                },
            ],
        },
        {
            "name": "Samsung Galaxy Z Flip5",
            "slug": "samsung-galaxy-z-flip-5",
            "category": galaxy_z,
            "short_description": "Compact foldable with large Flex Window cover screen.",
            "description": (
                "Galaxy Z Flip5 brings a pocket‑sized foldable design with a large cover screen for widgets, "
                "selfies and quick controls without unfolding the phone."
            ),
            "features": [
                "6.7\" FHD+ Dynamic AMOLED 2X inner display",
                "3.4\" Flex Window cover display",
                "Snapdragon 8 Gen 2 for Galaxy",
                "3700mAh battery",
                "FlexCam and hands‑free shooting modes",
            ],
            "variants": [
                {
                    "name": "256GB / 8GB",
                    "model_code": "SM-F731B-256",
                    "price": 149999,
                    "sale_price": None,
                    "stock_quantity": 20,
                    "specs": [],
                },
                {
                    "name": "512GB / 8GB",
                    "model_code": "SM-F731B-512",
                    "price": 169999,
                    "sale_price": None,
                    "stock_quantity": 12,
                    "specs": [],
                },
            ],
        },
        # ───────── Smartphones – Galaxy A (popular midrange) ─────────
        {
            "name": "Samsung Galaxy A55 5G",
            "slug": "samsung-galaxy-a55",
            "category": galaxy_a,
            "short_description": "Premium A‑series phone with AMOLED and OIS camera.",
            "description": (
                "Galaxy A55 5G offers a bright 6.6‑inch Super AMOLED display, large battery and OIS main camera "
                "for smooth everyday performance and social‑ready photos."
            ),
            "features": [
                "6.6\" FHD+ Super AMOLED 120Hz",
                "50MP triple rear camera with OIS",
                "32MP selfie camera",
                "5000mAh battery with 25W fast charging",
                "IP67 dust and water resistance",
            ],
            "variants": [
                {
                    "name": "128GB / 8GB",
                    "model_code": "SM-A556B-128",
                    "price": 58999,
                    "sale_price": None,
                    "stock_quantity": 40,
                    "specs": [],
                },
                {
                    "name": "256GB / 12GB",
                    "model_code": "SM-A556B-256",
                    "price": 65999,
                    "sale_price": None,
                    "stock_quantity": 25,
                    "specs": [],
                },
            ],
        },
        {
            "name": "Samsung Galaxy A35 5G",
            "slug": "samsung-galaxy-a35",
            "category": galaxy_a,
            "short_description": "Value 5G phone with AMOLED and big battery.",
            "description": (
                "Galaxy A35 5G balances performance, camera quality and battery life with a 6.6‑inch Super AMOLED "
                "display and 5000mAh battery."
            ),
            "features": [
                "6.6\" FHD+ Super AMOLED 120Hz",
                "50MP triple camera",
                "5000mAh battery",
                "IP67 dust and water resistance",
            ],
            "variants": [
                {
                    "name": "128GB / 6GB",
                    "model_code": "SM-A356B-128-6",
                    "price": 43999,
                    "sale_price": None,
                    "stock_quantity": 50,
                    "specs": [],
                },
                {
                    "name": "256GB / 8GB",
                    "model_code": "SM-A356B-256-8",
                    "price": 49999,
                    "sale_price": None,
                    "stock_quantity": 35,
                    "specs": [],
                },
            ],
        },
        {
            "name": "Samsung Galaxy A25 5G",
            "slug": "samsung-galaxy-a25",
            "category": galaxy_a,
            "short_description": "Affordable 5G Galaxy with AMOLED display.",
            "description": (
                "Galaxy A25 5G brings a 6.5‑inch Super AMOLED display, 50MP camera and long‑lasting battery "
                "to the affordable 5G segment."
            ),
            "features": [
                "6.5\" FHD+ Super AMOLED 90Hz",
                "50MP triple camera with OIS",
                "5000mAh battery",
                "Exynos 1280 processor",
            ],
            "variants": [
                {
                    "name": "128GB / 6GB",
                    "model_code": "SM-A256B-128-6",
                    "price": 31999,
                    "sale_price": None,
                    "stock_quantity": 60,
                    "specs": [],
                },
                {
                    "name": "128GB / 8GB",
                    "model_code": "SM-A256B-128-8",
                    "price": 34999,
                    "sale_price": None,
                    "stock_quantity": 40,
                    "specs": [],
                },
            ],
        },
        {
            "name": "Samsung Galaxy A15 4G",
            "slug": "samsung-galaxy-a15",
            "category": galaxy_a,
            "short_description": "Entry Galaxy with big battery and triple camera.",
            "description": (
                "Galaxy A15 offers a 6.5‑inch display, triple camera and 5000mAh battery at an entry‑friendly price."
            ),
            "features": [
                "6.5\" FHD+ Super AMOLED 90Hz",
                "50MP triple camera",
                "5000mAh battery with 25W fast charging",
            ],
            "variants": [
                {
                    "name": "128GB / 4GB",
                    "model_code": "SM-A155F-128-4",
                    "price": 22999,
                    "sale_price": None,
                    "stock_quantity": 70,
                    "specs": [],
                },
                {
                    "name": "128GB / 6GB",
                    "model_code": "SM-A155F-128-6",
                    "price": 25999,
                    "sale_price": None,
                    "stock_quantity": 50,
                    "specs": [],
                },
            ],
        },
        # ───────── Tablets – Galaxy Tab ─────────
        {
            "name": "Samsung Galaxy Tab S9 Ultra",
            "slug": "samsung-galaxy-tab-s9-ultra",
            "category": tab_s,
            "short_description": "Flagship 14.6\" AMOLED tablet with S Pen.",
            "description": (
                "Galaxy Tab S9 Ultra is Samsung's top‑tier tablet with a massive 14.6‑inch Dynamic AMOLED 2X display, "
                "Snapdragon 8 Gen 2 for Galaxy and S Pen in the box."
            ),
            "features": [
                "14.6\" Dynamic AMOLED 2X 120Hz",
                "Snapdragon 8 Gen 2 for Galaxy",
                "S Pen included in the box",
                "IP68 water and dust resistance (tablet + S Pen)",
                "Quad speakers with Dolby Atmos",
            ],
            "variants": [
                {
                    "name": "256GB / 12GB",
                    "model_code": "SM-X910-256-12",
                    "price": 169999,
                    "sale_price": None,
                    "stock_quantity": 15,
                    "specs": [],
                },
                {
                    "name": "512GB / 12GB",
                    "model_code": "SM-X910-512-12",
                    "price": 189999,
                    "sale_price": None,
                    "stock_quantity": 10,
                    "specs": [],
                },
            ],
        },
        {
            "name": "Samsung Galaxy Tab A9+",
            "slug": "samsung-galaxy-tab-a9-plus",
            "category": tab_a,
            "short_description": "Affordable large‑screen tablet for entertainment and study.",
            "description": (
                "Galaxy Tab A9+ delivers a large 11‑inch display, quad speakers and long battery life "
                "for streaming, learning and light productivity."
            ),
            "features": [
                "11\" LCD display 90Hz",
                "Quad speakers with Dolby Atmos",
                "Long‑lasting battery",
                "Expandable storage via microSD",
            ],
            "variants": [
                {
                    "name": "64GB / 4GB Wi‑Fi",
                    "model_code": "SM-X210-64-4",
                    "price": 38999,
                    "sale_price": None,
                    "stock_quantity": 30,
                    "specs": [],
                },
                {
                    "name": "128GB / 8GB LTE",
                    "model_code": "SM-X216-128-8",
                    "price": 45999,
                    "sale_price": None,
                    "stock_quantity": 20,
                    "specs": [],
                },
            ],
        },
        # ───────── Wearables – Galaxy Watch & Fit ─────────
        {
            "name": "Samsung Galaxy Watch7",
            "slug": "samsung-galaxy-watch-7",
            "category": watch_series,
            "short_description": "Next‑gen Galaxy Watch with AI‑powered health insights.",
            "description": (
                "Galaxy Watch7 brings advanced health tracking, AI‑powered insights and Wear OS by Samsung "
                "in a sleek, everyday smartwatch design."
            ),
            "features": [
                "Wear OS powered by Samsung",
                "Advanced heart rate and ECG monitoring",
                "Body composition analysis",
                "Sleep tracking with coaching",
                "GPS, Bluetooth and optional LTE",
            ],
            "variants": [
                {
                    "name": "40mm Bluetooth",
                    "model_code": "SM-L305-40-BT",
                    "price": 34999,
                    "sale_price": None,
                    "stock_quantity": 40,
                    "specs": [],
                },
                {
                    "name": "44mm LTE",
                    "model_code": "SM-L315-44-LTE",
                    "price": 45999,
                    "sale_price": None,
                    "stock_quantity": 25,
                    "specs": [],
                },
            ],
        },
        {
            "name": "Samsung Galaxy Watch6 Classic",
            "slug": "samsung-galaxy-watch-6-classic",
            "category": watch_series,
            "short_description": "Rotating bezel smartwatch with premium design.",
            "description": (
                "Galaxy Watch6 Classic combines a stainless steel case and rotating bezel with advanced health "
                "tracking and Wear OS for a timeless smartwatch experience."
            ),
            "features": [
                "Rotating physical bezel",
                "Stainless steel case",
                "Heart rate, ECG and blood pressure monitoring (region‑dependent)",
                "Sleep and stress tracking",
            ],
            "variants": [
                {
                    "name": "43mm Bluetooth",
                    "model_code": "SM-R960-43-BT",
                    "price": 39999,
                    "sale_price": None,
                    "stock_quantity": 30,
                    "specs": [],
                },
                {
                    "name": "47mm LTE",
                    "model_code": "SM-R965-47-LTE",
                    "price": 49999,
                    "sale_price": None,
                    "stock_quantity": 20,
                    "specs": [],
                },
            ],
        },
        {
            "name": "Samsung Galaxy Fit3",
            "slug": "samsung-galaxy-fit-3",
            "category": fit_bands,
            "short_description": "Lightweight fitness band with big display.",
            "description": (
                "Galaxy Fit3 is a slim fitness tracker with a large AMOLED screen, multi‑day battery "
                "life and essential health tracking features."
            ),
            "features": [
                "Large AMOLED display",
                "Heart rate and sleep tracking",
                "Water resistant for swimming",
                "Multi‑day battery life",
            ],
            "variants": [
                {
                    "name": "Standard Band",
                    "model_code": "SM-R390-STD",
                    "price": 11999,
                    "sale_price": None,
                    "stock_quantity": 80,
                    "specs": [],
                }
            ],
        },
        # ───────── Mobile Accessories – Buds, Chargers, Cases ─────────
        {
            "name": "Samsung Galaxy Buds2 Pro",
            "slug": "samsung-galaxy-buds-2-pro",
            "category": earbuds_cat,
            "short_description": "Premium ANC earbuds with 24‑bit Hi‑Fi sound.",
            "description": (
                "Galaxy Buds2 Pro deliver immersive 24‑bit Hi‑Fi audio, intelligent ANC and 360 Audio "
                "in a compact, comfortable design tuned for Galaxy devices."
            ),
            "features": [
                "24‑bit Hi‑Fi sound with Samsung Seamless Codec",
                "Intelligent Active Noise Cancellation",
                "360 Audio with head tracking",
                "IPX7 water resistance (earbuds)",
                "Wireless charging case",
            ],
            "variants": [
                {
                    "name": "Graphite",
                    "model_code": "SM-R510-GRA",
                    "price": 24999,
                    "sale_price": None,
                    "stock_quantity": 60,
                    "specs": [],
                },
                {
                    "name": "White",
                    "model_code": "SM-R510-WHT",
                    "price": 24999,
                    "sale_price": None,
                    "stock_quantity": 50,
                    "specs": [],
                },
            ],
        },
        {
            "name": "Samsung 45W Super Fast Charger",
            "slug": "samsung-45w-super-fast-charger",
            "category": chargers_cables,
            "short_description": "45W USB‑C charger for compatible Galaxy phones and tablets.",
            "description": (
                "Official Samsung 45W USB‑C Super Fast Charger for compatible Galaxy S and Galaxy Tab devices, "
                "supporting USB‑PD and PPS standards."
            ),
            "features": [
                "Up to 45W charging for compatible devices",
                "USB‑C to USB‑C cable included",
                "Supports USB Power Delivery (PD) and PPS",
                "Optimized for Galaxy S and Galaxy Tab flagships",
            ],
            "variants": [
                {
                    "name": "45W Charger + 1m Cable",
                    "model_code": "EP-T4510XWE",
                    "price": 7999,
                    "sale_price": None,
                    "stock_quantity": 100,
                    "specs": [],
                }
            ],
        },
        {
            "name": "Smart Clear View Case for Galaxy S24 Ultra",
            "slug": "smart-clear-view-case-s24-ultra",
            "category": phone_cases,
            "short_description": "Flip case with interactive view window for S24 Ultra.",
            "description": (
                "Official Smart Clear View Case for Galaxy S24 Ultra, offering full‑screen protection and "
                "a transparent window for notifications and calls."
            ),
            "features": [
                "Interactive clear view window",
                "Edge‑to‑edge front and back protection",
                "Optimized fit for Galaxy S24 Ultra",
            ],
            "variants": [
                {
                    "name": "Black",
                    "model_code": "EF-ZS928CBEG",
                    "price": 9999,
                    "sale_price": None,
                    "stock_quantity": 40,
                    "specs": [],
                },
                {
                    "name": "White",
                    "model_code": "EF-ZS928CWEG",
                    "price": 9999,
                    "sale_price": None,
                    "stock_quantity": 30,
                    "specs": [],
                },
            ],
        },
    ]

    created_count = 0
    updated_count = 0

    with transaction.atomic():
        for pdata in products_data:
            product, created = Product.objects.get_or_create(
                slug=pdata["slug"],
                defaults={
                    "category": pdata["category"],
                    "name": pdata["name"],
                    "short_description": pdata["short_description"],
                    "description": pdata["description"],
                    "features": pdata["features"],
                    "warranty_period": pdata.get("warranty_period", 24),
                    "is_featured": pdata.get("is_featured", False),
                    "is_active": True,
                },
            )

            if not created:
                # Keep product up to date with script data
                product.category = pdata["category"]
                product.name = pdata["name"]
                product.short_description = pdata["short_description"]
                product.description = pdata["description"]
                product.features = pdata["features"]
                product.warranty_period = pdata.get("warranty_period", 24)
                product.is_featured = pdata.get("is_featured", False)
                product.is_active = True
                product.save()
                updated_count += 1
            else:
                created_count += 1

            # Variants and specifications
            for order, vdata in enumerate(pdata.get("variants", [])):
                variant, v_created = ProductVariant.objects.get_or_create(
                    product=product,
                    model_code=vdata["model_code"],
                    defaults={
                        "name": vdata["name"],
                        "price": vdata["price"],
                        "sale_price": vdata.get("sale_price"),
                        "stock_quantity": vdata.get("stock_quantity", 0),
                        "availability": "in_stock",
                    },
                )

                if not v_created:
                    variant.name = vdata["name"]
                    variant.price = vdata["price"]
                    variant.sale_price = vdata.get("sale_price")
                    variant.stock_quantity = vdata.get("stock_quantity", variant.stock_quantity)
                    variant.availability = "in_stock"
                    variant.save()

                # Variant‑specific specs
                specs = vdata.get("specs", [])
                for idx, (cat, name, value) in enumerate(specs):
                    ProductSpecification.objects.update_or_create(
                        product=product,
                        variant=variant,
                        category=cat,
                        name=name,
                        defaults={
                            "value": value,
                            "display_order": idx,
                        },
                    )

    print(f"Mobile & Wearables catalog seeded. Products created: {created_count}, updated: {updated_count}")


if __name__ == "__main__":
    seed_mobile_and_wearables()

