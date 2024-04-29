from django.test import TestCase
from .models import Recipe

class ProductTestCase(TestCase):
    def test_product_creation(self):
        product = Recipe.objects.create(
            name='Test Product',
            desc='This is a test product.'
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.desc, 'This is a test product.')