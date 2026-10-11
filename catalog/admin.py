from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Category, Brand, AttributeDefinition, Product, ProductImage, ProductAttributeValue, Order, OrderItem

class ProductImageInline(TabularInline):
    model = ProductImage
    fields = ('image', 'external_url', 'alt_text', 'sort_order')

class ProductAttributeValueInline(TabularInline):
    model = ProductAttributeValue
    extra = 0
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields['definition'].queryset = AttributeDefinition.objects.filter(category=obj.category)
        return formset
    extra = 1

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'is_active', 'sort_order')
    list_editable = ('is_active', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'brand', 'sku', 'category', 'subcategory', 'price', 'stock', 'status', 'is_featured', 'updated_at')
    list_filter = ('status', 'category', 'subcategory', 'brand', 'is_featured')
    list_editable = ('price', 'stock', 'status', 'is_featured')
    list_select_related = ('category',)
    search_fields = ('name', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    inlines = (ProductImageInline, ProductAttributeValueInline)
    fieldsets = (('Product', {'fields': ('category', 'subcategory', 'brand', 'name', 'slug', 'sku', 'short_description', 'description')}), ('Sales', {'fields': ('price', 'old_price', 'stock', 'status', 'is_featured')}), ('SEO', {'fields': ('seo_title', 'seo_description')}), ('Details', {'fields': ('specifications',)}))

@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name', 'is_active', 'sort_order')
    list_editable = ('is_active', 'sort_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(AttributeDefinition)
class AttributeDefinitionAdmin(ModelAdmin):
    list_display = ('name', 'category', 'unit', 'is_filterable', 'sort_order')
    list_filter = ('category', 'is_filterable')
    prepopulated_fields = {'slug': ('name',)}

class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'unit_price', 'quantity')
    can_delete = False

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('number', 'customer_name', 'phone', 'total', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('number', 'customer_name', 'phone')
    readonly_fields = ('number', 'total', 'created_at')
    inlines = (OrderItemInline,)
