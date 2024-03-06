from django.urls import path
from .views import BuyItemView, ItemView, OrderView, BuyOrderView

from . import views




urlpatterns = [
    path('item/<int:pk>/', ItemView.as_view(), name='item-detail'),
    path('buy/<int:pk>/', BuyItemView.as_view(), name='buy-item'),
    path('cart/', OrderView.as_view(), name='cart-list'),
    path('add-to-cart/<int:item_id>/', OrderView.as_view(), name='add-to-cart'),
    path('success/', views.successful, name='success'),
    path('cancel/', views.canceled, name='cancel'),
    path('buy-cart/', BuyOrderView.as_view(), name='buy-all'),
]