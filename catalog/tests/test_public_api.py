from django.test import TestCase
from rest_framework.test import APIClient

from catalog.models import Brand, Category, Product


class PublicApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        category = Category.objects.create(name='Енергія', slug='energy')
        brand = Brand.objects.create(name='Baseus', slug='baseus')
        self.product = Product.objects.create(
            category=category, brand=brand, name='Powerbank', slug='powerbank', sku='TEST-POWERBANK',
            short_description='Тестовий товар', description='Опис', price=1000, stock=3,
            status=Product.Status.PUBLISHED,
        )

    def test_health_endpoint(self):
        response = self.client.get('/api/v1/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'ok')

    def test_order_reduces_stock_once_for_idempotent_request(self):
        payload = {'customer_name': 'Ірина', 'phone': '067 000 00 00', 'items': [{'slug': 'powerbank', 'quantity': 2}]}
        headers = {'HTTP_IDEMPOTENCY_KEY': '58f677d6-766c-4b2e-91d9-2adf51ed0b90'}
        first = self.client.post('/api/v1/orders/', payload, format='json', **headers)
        second = self.client.post('/api/v1/orders/', payload, format='json', **headers)
        self.product.refresh_from_db()
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(first.data['number'], second.data['number'])
        self.assertEqual(self.product.stock, 1)

    def test_order_rejects_invalid_phone(self):
        response = self.client.post('/api/v1/orders/', {'customer_name': 'Ірина', 'phone': '123', 'items': [{'slug': 'powerbank', 'quantity': 1}]}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone', response.data)
