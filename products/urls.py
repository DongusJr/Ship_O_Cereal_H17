from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductLogic.as_view(), name='product_index'),
    path('<int:id>', views.SingleProduct.as_view(), name='product_detail'),
    path('create_product', views.create_product, name='create_product'),
    path('update_product/<int:id>', views.update_product, name='update_product')
]