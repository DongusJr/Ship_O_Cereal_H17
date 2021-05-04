from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductLogic.as_view(), name='product_index'),
    path('<int:id>', views.get_product_by_id, name='product_detail')
]