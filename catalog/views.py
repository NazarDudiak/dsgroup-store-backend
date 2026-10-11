from uuid import UUID
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Order, Product
from .serializers import CategorySerializer, ProductCardSerializer, ProductDetailSerializer, OrderCreateSerializer

class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True)
class ProductList(generics.ListAPIView):
    serializer_class = ProductCardSerializer
    def get_queryset(self):
        qs = Product.objects.filter(status=Product.Status.PUBLISHED).select_related('category', 'subcategory_ref', 'brand').prefetch_related('images', 'attribute_values__definition')
        category, subcategory, q, featured = self.request.query_params.get('category'), self.request.query_params.get('subcategory'), self.request.query_params.get('q'), self.request.query_params.get('featured')
        brands = self.request.query_params.getlist('brand')
        if category: qs = qs.filter(category__slug=category)
        if subcategory: qs = qs.filter(Q(subcategory_ref__slug=subcategory) | Q(subcategory=subcategory))
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
    queryset = Product.objects.filter(status=Product.Status.PUBLISHED).select_related('category', 'subcategory_ref', 'brand').prefetch_related('images', 'attribute_values__definition')
class OrderCreate(APIView):
    throttle_scope = 'order'
    throttle_classes = [ScopedRateThrottle]
    def post(self, request):
        token = request.headers.get('Idempotency-Key', '')
        try:
            request_token = UUID(token) if token else None
        except ValueError:
            return Response({'detail': 'Неправильний ключ повторного запиту.'}, status=status.HTTP_400_BAD_REQUEST)
        if request_token:
            existing = Order.objects.filter(request_token=request_token).first()
            if existing:
                return Response({'number': existing.number, 'total': existing.total}, status=status.HTTP_200_OK)
        data = request.data.copy()
        if request_token:
            data['request_token'] = str(request_token)
        serializer = OrderCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            order = serializer.save()
        except IntegrityError:
            order = Order.objects.get(request_token=request_token)
            return Response({'number': order.number, 'total': order.total}, status=status.HTTP_200_OK)
        return Response({'number': order.number, 'total': order.total}, status=status.HTTP_201_CREATED)

class Health(APIView):
    permission_classes = []
    def get(self, request):
        return Response({'status': 'ok', 'service': 'dsgroup-api'})
