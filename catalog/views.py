from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Product
from .serializers import CategorySerializer, ProductCardSerializer, ProductDetailSerializer, OrderCreateSerializer

class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True)
class ProductList(generics.ListAPIView):
    serializer_class = ProductCardSerializer
    def get_queryset(self):
        qs = Product.objects.filter(status=Product.Status.PUBLISHED).select_related('category').prefetch_related('images')
        category, subcategory, q, featured = self.request.query_params.get('category'), self.request.query_params.get('subcategory'), self.request.query_params.get('q'), self.request.query_params.get('featured')
        brands = self.request.query_params.getlist('brand')
        if category: qs = qs.filter(category__slug=category)
        if subcategory: qs = qs.filter(subcategory=subcategory)
        if q: qs = qs.filter(Q(name__icontains=q) | Q(short_description__icontains=q) | Q(brand__name__icontains=q))
        if brands: qs = qs.filter(brand__name__in=brands)
        for key, value in self.request.query_params.items():
            if key.startswith('attr_') and value:
                qs = qs.filter(attribute_values__definition__slug=key[5:], attribute_values__value=value)
        if featured == 'true': qs = qs.filter(is_featured=True)
        return qs
class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    queryset = Product.objects.filter(status=Product.Status.PUBLISHED).select_related('category').prefetch_related('images')
class OrderCreate(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({'number': order.number, 'total': order.total}, status=status.HTTP_201_CREATED)
