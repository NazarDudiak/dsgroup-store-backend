from django.core.management.base import BaseCommand
from catalog.models import AttributeDefinition, Brand, Category, Product, ProductAttributeValue, ProductImage, Subcategory


# Product galleries use model-specific source images. Never replace an image with
# a generic stock photo: a missing licensed photo is preferable to a misleading card.
PRODUCT_GALLERIES = {
    'BASEUS-AIRPOW-20K': ['https://media.cdn.kaufland.de/product-images/1024x1024/498fe718a534ee3ed155f8dbb624d3e9.jpg', 'https://media.icdn.hu/product/2024-11/651551/1779491_baseus-airpow-power-bank-20000mah-pd-20w-fekete.webp', 'https://assets.innpro.pl/9424/10994/8.jpg'],
    'PROOVE-HYPER-10K': ['https://img.telemart.ua/864421-1132231/proove-hyper-flux-plus-10000mah-225w-pbf122120001-black.jpg'],
    'HOCO-J122A-20K': ['https://cdn.27.ua/sc--media--prod/default/27/e7/e8/27e7e831-4ed0-4aea-8c8f-0584fef13310.jpg', 'https://www.teq.com.au/cdn/shop/files/J122A-13.jpg?crop=center&height=800&width=800', 'https://www.teq.com.au/cdn/shop/files/J122A-8.jpg?crop=center&height=800&width=800'],
    'HOCO-W35-MAX': ['https://down-sg.img.susercontent.com/file/sg-11134201-7rbn5-loxn6s6adihpd2'],
    'BASEUS-MA10-PRO': ['https://down-my.img.susercontent.com/file/cn-11134207-7r98o-lt4nkup6wsm5f3'],
    'HOCO-EQ3-TWS': ['https://down-th.img.susercontent.com/file/th-11134207-7r990-lqbugayapq8q60', 'https://phukienhoco.vn/data/Product/tai-nghe-bt-khong-day-thuc-su-thong-minh-eq3-JOlrAZnt3IaQwcocHOf1.jpg', 'https://down-vn.img.susercontent.com/file/vn-11134207-7r98o-lsmz426pzjx5e7'],
    'JBL-GO4-BLU': ['https://www.jbl.com.mx/dw/image/v2/BFND_PRD/on/demandware.static/-/Sites-masterCatalog_Harman/default/dw4b7e6f14/JBL_GO_4_3_4_LEFT_BLUE_48173_x1.png?sh=1605&sw=1605', 'https://jblonlinestore.com.my/cdn/shop/files/BlueGO_4_8e599a36-97ce-4ed8-bd5e-250bb12e6863_large.png?v=1724314696'],
    'HOCO-HC22': ['https://file.hstatic.net/1000198144/file/dsc01786_1__3730b615277b4d0fa2deb7bffeda6cd4_1024x1024.jpg', 'https://down-th.img.susercontent.com/file/th-11134208-7r98y-lwqqu40yuqj3ae'],
    'BASEUS-GAN5-65W': ['https://media.falabella.com/falabellaPE/132523494_01/w%3D1500%2Ch%3D1500%2Cfit%3Dcover', 'https://media.falabella.com/falabellaPE/132523494_06/w%3D1500%2Ch%3D1500%2Cfit%3Dcover', 'https://cdn.shopify.com/s/files/1/0267/3534/5709/files/a-12_1024x1024.jpg?v=1694879610'],
    'BASEUS-CAFULE-C-2M': ['https://product.hstatic.net/200000685523/product/cap_type_c_baseus_cafule_cable_2m__c714__353ac0f0c83d4e11a32d66926fc25bcc_grande.png', 'https://baseus.com.au/cdn/shop/files/catklf-c91_400x.jpg?v=1749287293', 'https://mrcleaner.pl/img/imagecache/44001-45000/1026x1026_product_media_44001-45000_Baseus_Szybki_kabel_USB_USB_C_2m_2.webp'],
    'BASEUS-MINI3-15W': ['https://www.baseus.com/cdn/shop/products/CCJJ040001_Baseus_Simple_Mini3_Magnetic_Wireless_Charger_15W6_400x.jpg?v=1676026642', 'https://baseus.co.za/cdn/shop/files/9e82c38cc160cee989d07df64e31a871_752fa352-06e0-490c-b094-302d4f9943f0.jpg?v=1720955306&width=2000', 'https://content.rozetka.com.ua/goods/images/big/458578509.jpg'],
    'BASEUS-GOLDEN-40W': ['https://www.gadgetstore.qa/cdn/shop/files/dual-car-charger-baseus-golden-contractor-pro-gadget-store-quick-usb-40w-313.jpg?v=1690791681'],
    'ECOFLOW-RIVER-2': ['https://down-id.img.susercontent.com/file/sg-11134201-7rato-mb27q1ejrfqac3'],
    'ECOFLOW-110W': ['https://ecommerce.datablitz.com.ph/cdn/shop/files/GHFGFNNCV_1600x.jpg?v=1733985561', 'https://down-th.img.susercontent.com/file/th-11134207-7ras8-m8065v31vc32a3', 'https://down-my.img.susercontent.com/file/cn-11134207-820l4-ml4fstno1ybnc7'],
    'LOGICPOWER-LPM-U625VA': ['https://kompas.dp.ua/content/images/6/1000x1000l80nn0/copy_ybp-logicpower-lpy-psw-800va-560vt-5a-15a-s-pravylnoi-synusoydoi-12v-4153705-14066389982748.png'],
}

SUBCATEGORIES = {
    'BASEUS-AIRPOW-20K': 'powerbanks', 'PROOVE-HYPER-10K': 'powerbanks', 'HOCO-J122A-20K': 'powerbanks',
    'ECOFLOW-RIVER-2': 'charging-stations', 'ECOFLOW-110W': 'solar-chargers', 'LOGICPOWER-LPM-U625VA': 'ups',
    'HOCO-W35-MAX': 'over-ear-headphones', 'BASEUS-MA10-PRO': 'wireless-headphones', 'HOCO-EQ3-TWS': 'wireless-headphones', 'JBL-GO4-BLU': 'portable-speakers', 'HOCO-HC22': 'portable-speakers',
    'BASEUS-GAN5-65W': 'wall-chargers', 'BASEUS-CAFULE-C-2M': 'usb-cables', 'BASEUS-MINI3-15W': 'wireless-chargers', 'BASEUS-GOLDEN-40W': 'car-chargers',
}

RETIRED_SKUS = ('HOCO-J122B-20K', 'BASEUS-BLADE-100W', 'PROOVE-ZERO-PRO', 'HOCO-X88-C', 'PROOVE-RAPID-20W', 'BASEUS-CAFULE-C')

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
            ('energy', 'Hoco J122A Respect 20 000 mAh', 'HOCO-J122A-20K', 'Павербанк з PD20W та QC 22.5W для швидкого резервного живлення.', 1399, 1599, 'power', {'Ємність': '20 000 mAh', 'Потужність': '22.5W / PD20W', 'Порти': 'USB-C, 2×USB-A'}),
            ('energy', 'EcoFlow RIVER 2 256Wh', 'ECOFLOW-RIVER-2', 'Портативна зарядна станція 300W з LiFePO₄-акумулятором.', 10999, None, 'power', {'Ємність': '256 Wh', 'Номінальна потужність': '300W', 'Тип батареї': 'LiFePO₄'}),
            ('energy', 'EcoFlow 110W Portable Solar Panel', 'ECOFLOW-110W', 'Складана сонячна панель для автономного живлення.', 8999, None, 'power', {'Потужність': '110W', 'Захист': 'IP68', 'Тип': 'Складана'}),
            ('energy', 'LogicPower LPM-U625VA', 'LOGICPOWER-LPM-U625VA', 'Лінійно-інтерактивне ДБЖ для роутера, ПК або робочого місця.', 2557, None, 'power', {'Потужність': '625 VA / 437 W', 'Тип': 'Line-interactive', 'Акумулятор': '7.5 Ah'}),
            ('audio', 'Hoco W35 Max Bluetooth', 'HOCO-W35-MAX', 'Повнорозмірні Bluetooth-навушники з 40 мм динаміками.', 899, 1099, 'audio', {'Підключення': 'Bluetooth 5.3', 'Робота': 'до 90 год', 'Мікрофон': 'Так'}),
            ('audio', 'Baseus Bowie MA10 Pro', 'BASEUS-MA10-PRO', 'TWS-навушники з активним шумозаглушенням.', 1799, None, 'audio', {'Підключення': 'Bluetooth 5.3', 'Захист': 'IPX6', 'Робота': 'до 140 год'}),
            ('audio', 'Hoco EQ3 TWS', 'HOCO-EQ3-TWS', 'Легкі навушники в зарядному кейсі.', 699, 799, 'audio', {'Підключення': 'Bluetooth 5.3', 'Робота': 'до 20 год', 'Керування': 'Сенсорне'}),
            ('audio', 'JBL Go 4 Blue', 'JBL-GO4-BLU', 'Ультрапортативна колонка JBL Pro Sound із захистом IP67.', 2299, None, 'audio', {'Підключення': 'Bluetooth 5.3', 'Захист': 'IP67', 'Робота': 'до 7 год'}),
            ('audio', 'Hoco HC22', 'HOCO-HC22', 'Компактна Bluetooth-колонка 5W з ремінцем для перенесення.', 799, None, 'audio', {'Підключення': 'Bluetooth 5.2', 'Потужність': '5W', 'Робота': 'до 4 год'}),
            ('charging', 'Baseus GaN5 Pro 65W', 'BASEUS-GAN5-65W', 'GaN-зарядка для смартфона, планшета і ноутбука.', 1599, None, 'cable', {'Потужність': '65W', 'Порти': '2×USB-C, USB-A', 'Технологія': 'GaN'}),
            ('charging', 'Baseus Cafule USB-A to USB-C 2 м', 'BASEUS-CAFULE-C-2M', 'Посилений кабель CATKLF-C в нейлоновому обплетенні.', 329, None, 'cable', {'Довжина': '2 м', 'Струм': '2A', 'Роз’єм': 'USB-A → USB-C'}),
            ('charging', 'Baseus Simple Mini3 Magnetic 15W', 'BASEUS-MINI3-15W', 'Магнітна бездротова зарядка для сумісних смартфонів.', 914, None, 'cable', {'Потужність': '15W', 'Інтерфейс': 'USB-C', 'Тип': 'Магнітна'}),
            ('charging', 'Baseus Golden Contactor Pro 40W', 'BASEUS-GOLDEN-40W', 'Двопортова автомобільна зарядка з швидким заряджанням.', 699, None, 'cable', {'Потужність': '40W', 'Порти': '2×USB', 'Призначення': 'Автомобільна'}),
        ]
        Product.objects.filter(sku__in=RETIRED_SKUS).update(status=Product.Status.DRAFT, is_featured=False)
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
            gallery = PRODUCT_GALLERIES[sku]
            for position, url in enumerate(gallery):
                ProductImage.objects.create(product=product, external_url=url, alt_text=name, sort_order=position)
        self.stdout.write(self.style.SUCCESS('DSGroup demo catalogue created.'))
