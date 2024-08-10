# store/management/commands/import_products.py

import json
import os
from django.core.management.base import BaseCommand
from store.models import Product, Category, ProductImage
from django.conf import settings

class Command(BaseCommand):
    help = 'Import products and images from a JSON file'

    def handle(self, *args, **kwargs):
        # Load JSON data
        json_file_path = os.path.join(settings.BASE_DIR, 'store', 'products_data.json')
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        for item in data:
            category, created = Category.objects.get_or_create(name=item['category'])

            product = Product.objects.create(
                name=item['name'],
                description=item['description'],
                price=item['price'],
                category=category
            )

            for image_path in item['images']:
                image_path = os.path.join(settings.BASE_DIR, image_path)
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as image_file:
                        ProductImage.objects.create(
                            product=product,
                            image=image_file.read()  # Assumes ProductImage model has an ImageField
                        )

        self.stdout.write(self.style.SUCCESS('Products imported successfully!'))
