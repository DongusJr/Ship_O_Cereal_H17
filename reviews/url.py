from django.contrib.auth.views import LogoutView
from django.urls import path
from reviews import views

urlpatterns = [
    path('review', views.ReviewLogic.as_view(), name='review_form')
]