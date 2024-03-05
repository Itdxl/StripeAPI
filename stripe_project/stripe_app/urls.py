from django.urls import path
from .views import BuyItemView, ItemView

from . import views
# from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('item/<int:pk>/', ItemView.as_view(), name='item-detail'),
    path('buy/<int:pk>/', BuyItemView.as_view(), name='buy-item'),
    path('success/', views.successful, name='success'),
    path('cancel/', views.canceled, name='cancel'),

]
