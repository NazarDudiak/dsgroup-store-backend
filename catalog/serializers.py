import re
from django.db import transaction
from rest_framework import serializers
from .models import AttributeDefinition, Category, Product, ProductAttributeValue, ProductImage, Order, OrderItem, Subcategory

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta: model = ProductImage; fields = ('image', 'alt_text')
    def get_image(self, obj):
        return obj.image.url if obj.image else obj.external_url
class AttributeValueSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='definition.name', read_only=True)
    slug = serializers.CharField(source='definition.slug', read_only=True)
    unit = serializers.CharField(source='definition.unit', read_only=True)
    is_filterable = serializers.BooleanField(source='definition.is_filterable', read_only=True)
    class Meta: model = ProductAttributeValue; fields = ('name', 'slug', 'unit', 'value', 'is_filterable')

class SubcategorySerializer(serializers.ModelSerializer):
    brands = serializers.SerializerMethodField()
    class Meta: model = Subcategory; fields = ('name', 'slug', 'description', 'seo_title', 'seo_description', 'brands')
    def get_brands(self, obj):
        return list(obj.products.filter(status=Product.Status.PUBLISHED, brand__is_active=True).exclude(brand=None).order_by('brand__name').values_list('brand__name', flat=True).distinct())

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    class Meta: model = Category; fields = ('name', 'slug', 'description', 'image', 'seo_title', 'seo_description', 'subcategories')
    def get_subcategories(self, obj):
        return SubcategorySerializer(obj.subcategories.filter(is_active=True), many=True).data
class ProductCardSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    brand = serializers.CharField(source='brand.name', read_only=True)
    image = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, read_only=True)
    subcategory = serializers.SerializerMethodField()
    attributes = AttributeValueSerializer(source='attribute_values', many=True, read_only=True)
    class Meta: model = Product; fields = ('name', 'slug', 'sku', 'short_description', 'price', 'old_price', 'stock', 'category', 'subcategory', 'brand', 'image', 'images', 'attributes')
    def get_image(self, obj):
        first = obj.images.first()
        return (first.image.url if first.image else first.external_url) if first else None
    def get_subcategory(self, obj):
        return obj.subcategory_ref.slug if obj.subcategory_ref_id else obj.subcategory
class ProductDetailSerializer(ProductCardSerializer):
    class Meta(ProductCardSerializer.Meta): fields = ProductCardSerializer.Meta.fields + ('description', 'seo_title', 'seo_description')
class OrderCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=120)
    phone = serializers.CharField(max_length=32)
    email = serializers.EmailField(required=False, allow_blank=True)
    comment = serializers.CharField(required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(choices=Order.PaymentMethod.choices, default=Order.PaymentMethod.COD)
    items = serializers.ListField(child=serializers.DictField(), min_length=1, max_length=20)
    request_token = serializers.UUIDField(required=False, write_only=True)
    def validate_phone(self, value):
        normalized = re.sub(r'[^0-9+]', '', value)
        if normalized.startswith('0') and len(normalized) == 10:
            normalized = '+38' + normalized
        elif normalized.startswith('380') and len(normalized) == 12:
            normalized = '+' + normalized
        if not re.fullmatch(r'\+380\d{9}', normalized):
            raise serializers.ValidationError('Вкажіть український номер у форматі +380XXXXXXXXX.')
        return normalized
    def create(self, data):
        items = data.pop('items')
        with transaction.atomic():
            order = Order.objects.create(**data)
            total = 0
            for row in items:
                try:
                    product = Product.objects.select_for_update().get(slug=row['slug'], status=Product.Status.PUBLISHED)
                    quantity = int(row.get('quantity', 1))
                except (Product.DoesNotExist, KeyError, TypeError, ValueError):
                    raise serializers.ValidationError({'items': 'Один або кілька товарів недоступні.'})
                if quantity < 1 or quantity > product.stock:
                    raise serializers.ValidationError({'items': f'Недостатньо товару: {product.name}.'})
                OrderItem.objects.create(order=order, product=product, product_name=product.name, unit_price=product.price, quantity=quantity)
                total += product.price * quantity
                product.stock -= quantity
                product.save(update_fields=['stock', 'updated_at'])
            order.total = total
            order.save(update_fields=['total'])
            return order
