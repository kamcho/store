import os
import sys
import django

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Find the Django settings module
def find_settings():
    # Look for a folder containing settings.py (e.g., 'Samsung', 'store', etc.)
    for item in os.listdir(BASE_DIR):
        if os.path.isdir(os.path.join(BASE_DIR, item)) and os.path.exists(os.path.join(BASE_DIR, item, 'settings.py')):
            return f"{item}.settings"
    return "Samsung.settings" # Fallback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', find_settings())
django.setup()
