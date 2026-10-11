from rest_framework import serializers
from .models import Category, Product, ProductImage, Order, OrderItem

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta: model = ProductImage; fields = ('image', 'alt_text')
    def get_image(self, obj):
        return obj.image.url if obj.image else obj.external_url
class CategorySerializer(serializers.ModelSerializer):
    class Meta: model = Category; fields = ('name', 'slug', 'description', 'image', 'seo_title', 'seo_description')
class ProductCardSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    brand = serializers.CharField(source='brand.name', read_only=True)
    image = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, read_only=True)
    class Meta: model = Product; fields = ('name', 'slug', 'sku', 'short_description', 'price', 'old_price', 'stock', 'category', 'subcategory', 'brand', 'specifications', 'image', 'images')
    def get_image(self, obj):
        first = obj.images.first()
        return (first.image.url if first.image else first.external_url) if first else None
class ProductDetailSerializer(ProductCardSerializer):
    class Meta(ProductCardSerializer.Meta): fields = ProductCardSerializer.Meta.fields + ('description', 'seo_title', 'seo_description')
class OrderCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=120)
    phone = serializers.CharField(max_length=32)
    email = serializers.EmailField(required=False, allow_blank=True)
    comment = serializers.CharField(required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(choices=Order.PaymentMethod.choices, default=Order.PaymentMethod.COD)
    items = serializers.ListField(child=serializers.DictField(), min_length=1, max_length=20)
    def create(self, data):
        items = data.pop('items')
        order = Order.objects.create(**data)
        total = 0
        for row in items:
            try: product = Product.objects.get(slug=row['slug'], status=Product.Status.PUBLISHED)
            except (Product.DoesNotExist, KeyError): raise serializers.ValidationError({'items': 'One or more products are unavailable.'})
            quantity = int(row.get('quantity', 1))
            if quantity < 1 or quantity > product.stock: raise serializers.ValidationError({'items': f'Insufficient stock for {product.name}.'})
            OrderItem.objects.create(order=order, product=product, product_name=product.name, unit_price=product.price, quantity=quantity)
            total += product.price * quantity
            product.stock -= quantity; product.save(update_fields=['stock', 'updated_at'])
        order.total = total; order.save(update_fields=['total'])
        return order
