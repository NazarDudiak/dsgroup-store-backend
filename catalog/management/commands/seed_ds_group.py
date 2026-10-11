from django.core.management.base import BaseCommand
from catalog.models import AttributeDefinition, Brand, Category, Product, ProductAttributeValue, ProductImage, Subcategory


IMAGES = {
    'power': ['https://eu.baseus.com/cdn/shop/products/Baseus_Airpow_Power_Bank_20W_20000mAh_1_front_side_1100x.jpg?v=1688625444', 'https://www.baseus.com/cdn/shop/files/Baseus_Airpow_Power_Bank_20W_10000mAh_Black_PPQD0900013_1200x.jpg?v=1684814771', 'https://img.telemart.ua/864421-1132231/proove-hyper-flux-plus-10000mah-225w-pbf122120001-black.jpg'],
    'audio': ['https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=85', 'https://images.unsplash.com/photo-1484704849700-f032a568e944?auto=format&fit=crop&w=1200&q=85', 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=1200&q=85'],
    'cable': ['https://images.unsplash.com/photo-1625723044792-44de16ccb4e9?auto=format&fit=crop&w=1200&q=85', 'https://images.unsplash.com/photo-1587033411391-5d9e51cce126?auto=format&fit=crop&w=1200&q=85', 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=1200&q=85'],
}

# The first photo is used on catalogue cards. Every SKU has its own image so
# cards are visually distinct; the remaining two form its temporary gallery.
CARD_IMAGES = {
    'BASEUS-AIRPOW-20K': 'https://eu.baseus.com/cdn/shop/products/Baseus_Airpow_Power_Bank_20W_20000mAh_1_front_side_1100x.jpg?v=1688625444',
    'PROOVE-HYPER-10K': 'https://img.telemart.ua/864421-1132231/proove-hyper-flux-plus-10000mah-225w-pbf122120001-black.jpg',
    'HOCO-J122B-20K': 'https://images.unsplash.com/photo-1609592424824-0e71d1c6c5ed?auto=format&fit=crop&w=1200&q=85',
    'BASEUS-BLADE-100W': 'https://images.unsplash.com/photo-1625671371213-6a7f3951c49f?auto=format&fit=crop&w=1200&q=85',
    'HOCO-W35-MAX': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1200&q=85',
    'BASEUS-MA10-PRO': 'https://images.unsplash.com/photo-1484704849700-f032a568e944?auto=format&fit=crop&w=1200&q=85',
    'PROOVE-ZERO-PRO': 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=1200&q=85',
    'HOCO-EQ3-TWS': 'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?auto=format&fit=crop&w=1200&q=85',
    'BASEUS-GAN5-65W': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=1200&q=85',
    'HOCO-X88-C': 'https://images.unsplash.com/photo-1625723044792-44de16ccb4e9?auto=format&fit=crop&w=1200&q=85',
    'PROOVE-RAPID-20W': 'https://images.unsplash.com/photo-1558089687-f282ffcbc126?auto=format&fit=crop&w=1200&q=85',
    'BASEUS-CAFULE-C': 'https://images.unsplash.com/photo-1587033411391-5d9e51cce126?auto=format&fit=crop&w=1200&q=85',
}

SUBCATEGORIES = {
    'BASEUS-AIRPOW-20K': 'powerbanks', 'PROOVE-HYPER-10K': 'powerbanks', 'HOCO-J122B-20K': 'powerbanks', 'BASEUS-BLADE-100W': 'powerbanks',
    'HOCO-W35-MAX': 'over-ear-headphones', 'BASEUS-MA10-PRO': 'wireless-headphones', 'PROOVE-ZERO-PRO': 'wireless-headphones', 'HOCO-EQ3-TWS': 'wireless-headphones',
    'BASEUS-GAN5-65W': 'wall-chargers', 'HOCO-X88-C': 'usb-cables', 'PROOVE-RAPID-20W': 'wall-chargers', 'BASEUS-CAFULE-C': 'usb-cables',
}

SUBCATEGORY_DETAILS = {
    'energy': [('powerbanks', 'Павербанки'), ('charging-stations', 'Зарядні станції'), ('solar-chargers', 'Сонячні зарядні пристрої'), ('ups', 'Джерела безперебійного живлення')],
    'audio': [('wireless-headphones', 'Бездротові навушники'), ('over-ear-headphones', 'Повнорозмірні навушники'), ('portable-speakers', 'Портативна акустика')],
    'charging': [('wall-chargers', 'Мережеві зарядні пристрої'), ('usb-cables', 'Кабелі USB та USB-C'), ('wireless-chargers', 'Бездротові зарядні пристрої'), ('car-chargers', 'Автомобільні зарядки')],
}


class Command(BaseCommand):
    help = 'Create a DSGroup demo catalogue with temporary external product images.'

    def handle(self, *args, **options):
        categories = {}
        for name, slug, description in [
            ('Енергія для блекауту', 'energy', 'Павербанки, зарядні станції та все для автономності.'),
            ('Навушники та аудіо', 'audio', 'Бездротові навушники та портативний звук.'),
            ('Кабелі та зарядки', 'charging', 'Адаптери, кабелі й зарядні пристрої для щоденного використання.'),
        ]:
            categories[slug], _ = Category.objects.update_or_create(slug=slug, defaults={'name': name, 'description': description, 'is_active': True})
        subcategories = {}
        for category_slug, rows in SUBCATEGORY_DETAILS.items():
            for position, (slug, name) in enumerate(rows):
                subcategories[slug], _ = Subcategory.objects.update_or_create(
                    category=categories[category_slug], slug=slug,
                    defaults={'name': name, 'is_active': True, 'sort_order': position},
                )
        products = [
            ('energy', 'Baseus Airpow 20W 20 000 mAh', 'BASEUS-AIRPOW-20K', 'Потужний павербанк для смартфона та планшета.', 1599, 1899, 'power', {'Ємність': '20 000 mAh', 'Потужність': '20W PD', 'Порти': 'USB-C, 2×USB-A'}),
            ('energy', 'Proove Hyper Flux Plus 10 000 mAh', 'PROOVE-HYPER-10K', 'Швидка зарядка 22.5W у компактному корпусі.', 1199, None, 'power', {'Ємність': '10 000 mAh', 'Потужність': '22.5W', 'Порти': 'USB-C, USB-A'}),
            ('energy', 'Hoco J122B 20 000 mAh', 'HOCO-J122B-20K', 'Надійний резерв енергії на щодень і під час блекауту.', 1399, 1599, 'power', {'Ємність': '20 000 mAh', 'Індикатор': 'LED', 'Порти': 'USB-C, USB-A'}),
            ('energy', 'Baseus Blade 100W 20 000 mAh', 'BASEUS-BLADE-100W', 'Тонкий павербанк для ноутбука та всіх мобільних пристроїв.', 3499, None, 'power', {'Ємність': '20 000 mAh', 'Потужність': '100W', 'Екран': 'Цифровий'}),
            ('audio', 'Hoco W35 Max Bluetooth', 'HOCO-W35-MAX', 'Повнорозмірні навушники з м’якими амбушурами.', 899, 1099, 'audio', {'Підключення': 'Bluetooth 5.3', 'Робота': 'до 40 год', 'Мікрофон': 'Так'}),
            ('audio', 'Baseus Bowie MA10 Pro', 'BASEUS-MA10-PRO', 'TWS-навушники з активним шумозаглушенням.', 1799, None, 'audio', {'Підключення': 'Bluetooth 5.3', 'Захист': 'IPX6', 'Робота': 'до 140 год'}),
            ('audio', 'Proove Zero Pro', 'PROOVE-ZERO-PRO', 'Компактні бездротові навушники для дзвінків і музики.', 1299, None, 'audio', {'Підключення': 'Bluetooth 5.3', 'Робота': 'до 24 год', 'Мікрофон': 'ENC'}),
            ('audio', 'Hoco EQ3 TWS', 'HOCO-EQ3-TWS', 'Легкі навушники в зарядному кейсі.', 699, 799, 'audio', {'Підключення': 'Bluetooth 5.3', 'Робота': 'до 20 год', 'Керування': 'Сенсорне'}),
            ('charging', 'Baseus GaN5 Pro 65W', 'BASEUS-GAN5-65W', 'GaN-зарядка для смартфона, планшета і ноутбука.', 1599, None, 'cable', {'Потужність': '65W', 'Порти': '2×USB-C, USB-A', 'Технологія': 'GaN'}),
            ('charging', 'Hoco X88 USB-C 1 м', 'HOCO-X88-C', 'Міцний кабель USB-C для швидкої зарядки та синхронізації.', 199, None, 'cable', {'Довжина': '1 м', 'Струм': '3A', 'Роз’єм': 'USB-C'}),
            ('charging', 'Proove Rapid 20W', 'PROOVE-RAPID-20W', 'Компактний адаптер з PD для швидкого заряджання.', 499, 599, 'cable', {'Потужність': '20W PD', 'Порт': 'USB-C', 'Захист': 'Від перегріву'}),
            ('charging', 'Baseus Cafule USB-C 2 м', 'BASEUS-CAFULE-C', 'Посилений кабель у нейлоновому обплетенні.', 329, None, 'cable', {'Довжина': '2 м', 'Струм': '3A', 'Матеріал': 'Нейлон'}),
        ]
        for index, (category, name, sku, short, price, old_price, image_set, specs) in enumerate(products):
            brand_name = name.split()[0]
            brand, _ = Brand.objects.get_or_create(name=brand_name, defaults={'slug': brand_name.lower()})
            subcategory_slug = SUBCATEGORIES.get(sku, '')
            product, _ = Product.objects.update_or_create(sku=sku, defaults={'category': categories[category], 'subcategory': subcategory_slug, 'subcategory_ref': subcategories.get(subcategory_slug), 'brand': brand, 'name': name, 'slug': sku.lower(), 'short_description': short, 'description': f'{short} Перевірене рішення для щоденного використання та резерву під час відключень електроенергії.', 'price': price, 'old_price': old_price, 'stock': 12 + index, 'status': Product.Status.PUBLISHED, 'is_featured': index < 8, 'specifications': specs, 'seo_title': f'{name} — купити в DSGroup', 'seo_description': short})
            ProductAttributeValue.objects.filter(product=product).delete()
            for position, (label, value) in enumerate(specs.items()):
                definition, _ = AttributeDefinition.objects.get_or_create(category=categories[category], slug=label.lower().replace(' ', '-'), defaults={'name': label, 'is_filterable': True, 'sort_order': position})
                ProductAttributeValue.objects.create(product=product, definition=definition, value=str(value))
            ProductImage.objects.filter(product=product).delete()
            gallery = [CARD_IMAGES[sku], *[url for url in IMAGES[image_set] if url != CARD_IMAGES[sku]]]
            for position, url in enumerate(gallery):
                ProductImage.objects.create(product=product, external_url=url, alt_text=name, sort_order=position)
        self.stdout.write(self.style.SUCCESS('DSGroup demo catalogue created.'))
