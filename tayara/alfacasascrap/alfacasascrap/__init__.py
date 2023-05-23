import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alfacasascrap.settings')
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', 'true')
django.setup()