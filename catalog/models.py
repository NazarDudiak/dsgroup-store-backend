from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify

class SEOFields(models.Model):
    seo_title = models.CharField('SEO title', max_length=60, blank=True)
    seo_description = models.CharField('SEO description', max_length=160, blank=True)
    class Meta:
        abstract = True

class Category(SEOFields):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name_plural = 'Categories'
    def __str__(self): return self.name
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Subcategory(SEOFields):
    """A navigable catalogue level managed in the admin, not a free-text tag."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    class Meta:
        ordering = ['sort_order', 'name']
        constraints = [models.UniqueConstraint(fields=['category', 'slug'], name='unique_subcategory_per_category')]
    def __str__(self): return f'{self.category.name}: {self.name}'
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Brand(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering = ['sort_order', 'name']
    def __str__(self): return self.name

class AttributeDefinition(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attribute_definitions')
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    unit = models.CharField(max_length=20, blank=True)
    choices = models.JSONField(default=list, blank=True, help_text='List of options, e.g. ["10000", "20000"]')
    is_filterable = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    class Meta:
        ordering = ['sort_order', 'name']
        constraints = [models.UniqueConstraint(fields=['category', 'slug'], name='unique_attribute_per_category')]
    def __str__(self): return f'{self.category.name}: {self.name}'

class Product(SEOFields):
    class Status(models.TextChoices): DRAFT = 'draft', 'Draft'; PUBLISHED = 'published', 'Published'
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    subcategory = models.SlugField(max_length=80, blank=True, db_index=True, help_text='For example: powerbanks or over-ear-headphones.')
    subcategory_ref = models.ForeignKey(Subcategory, on_delete=models.PROTECT, related_name='products', null=True, blank=True, verbose_name='subcategory')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', null=True, blank=True)
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, max_length=200)
    sku = models.CharField(max_length=64, unique=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(default=False)
    specifications = models.JSONField(default=dict, blank=True, help_text='Example: {"Material": "Cotton"}')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-is_featured', '-updated_at']
        indexes = [models.Index(fields=['status', 'category']), models.Index(fields=['status', 'subcategory']), models.Index(fields=['slug'])]
    def __str__(self): return self.name
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values')
    definition = models.ForeignKey(AttributeDefinition, on_delete=models.PROTECT, related_name='product_values')
    value = models.CharField(max_length=120)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['product', 'definition'], name='unique_product_attribute')]
    def __str__(self): return f'{self.definition.name}: {self.value}'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', blank=True)
    external_url = models.URLField(blank=True, help_text='Temporary external image URL. Upload your own image before production.')
    alt_text = models.CharField(max_length=140, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering = ['sort_order', 'id']

class Order(models.Model):
    class Status(models.TextChoices): NEW = 'new', 'New'; CONFIRMED = 'confirmed', 'Confirmed'; SHIPPED = 'shipped', 'Shipped'; CANCELLED = 'cancelled', 'Cancelled'
    class PaymentMethod(models.TextChoices): COD = 'cod', 'Payment on delivery'; BANK = 'bank', 'Bank transfer'
    number = models.CharField(max_length=16, unique=True, editable=False)
    request_token = models.UUIDField(unique=True, null=True, blank=True, editable=False)
    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=32)
    email = models.EmailField(blank=True)
    comment = models.TextField(blank=True)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices, default=PaymentMethod.COD)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']
    def save(self, *args, **kwargs):
        if not self.number:
            from uuid import uuid4
            self.number = f'ORD-{uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)
    def __str__(self): return self.number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=180)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
