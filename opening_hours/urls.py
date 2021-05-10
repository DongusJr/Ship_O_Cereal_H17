from django.urls import path
from . import views

urlpatterns = [
    path('', views.OpeningHours.as_view(), name='opening_hours')
]