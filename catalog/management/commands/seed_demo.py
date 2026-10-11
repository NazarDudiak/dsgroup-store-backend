from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Create a small Ukrainian demo catalogue. Existing records are preserved.'

    def handle(self, *args, **options):
        home, _ = Category.objects.get_or_create(name='Для дому', slug='dlia-domu', defaults={'description': 'Практичні товари для затишного дому.', 'is_active': True})
        care, _ = Category.objects.get_or_create(name='Догляд', slug='dohliad', defaults={'description': 'Щоденний догляд.', 'is_active': True})
        rows = [
            (home, 'Аромасвічка Cedar', 'CANDLE-CEDAR', 'Теплий аромат кедра для вечірнього затишку.', 'Свічка з соєвого воску ручної роботи. Горить до 35 годин.', '590.00', {'Об’єм': '220 мл', 'Час горіння': '35 годин'}),
            (home, 'Керамічна чашка Oat', 'CUP-OAT', 'Матова чашка для улюбленої кави або чаю.', 'Виготовлена з кераміки, підходить для посудомийної машини.', '420.00', {'Об’єм': '350 мл', 'Матеріал': 'Кераміка'}),
            (care, 'Бальзам для рук', 'BALM-HAND', 'Живильний бальзам з натуральними оліями.', 'Швидко поглинається та залишає легкий трав’яний аромат.', '310.00', {'Об’єм': '50 мл', 'Тип шкіри': 'Усі типи'}),
        ]
        for category, name, sku, short, description, price, specs in rows:
            Product.objects.get_or_create(sku=sku, defaults={'category': category, 'name': name, 'slug': sku.lower(), 'short_description': short, 'description': description, 'price': price, 'stock': 20, 'status': Product.Status.PUBLISHED, 'is_featured': True, 'specifications': specs, 'seo_title': name, 'seo_description': short})
        self.stdout.write(self.style.SUCCESS('Demo catalogue created.'))
