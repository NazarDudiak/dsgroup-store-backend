from django.urls import path
from .views import CategoryList, ProductList, ProductDetail, OrderCreate, Health
urlpatterns = [path('health/', Health.as_view()), path('categories/', CategoryList.as_view()), path('products/', ProductList.as_view()), path('products/<slug:slug>/', ProductDetail.as_view()), path('orders/', OrderCreate.as_view())]
