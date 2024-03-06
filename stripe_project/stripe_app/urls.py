from django.urls import path
from .views import BuyItemView, ItemView, OrderView, CouponView, BuyOrderView

from . import views
# from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('item/<int:pk>/', ItemView.as_view(), name='item-detail'),
    path('buy/<int:pk>/', BuyItemView.as_view(), name='buy-item'),
    path('cart/', OrderView.as_view(), name='cart-list'),
    path('add-to-cart/<int:item_id>/', OrderView.as_view(), name='add-to-cart'),
    path('success/', views.successful, name='success'),
    path('cancel/', views.canceled, name='cancel'),
    # path('coupon/<int:pk>/', views.get_coupon, name ='get-coupon'),
    # path('coupons/',  CouponView.as_view(), name='coupons'),

    path('buy-cart/', BuyOrderView.as_view(), name='buy-item'),
    path('buy-cart/<int:pk>/', BuyOrderView.as_view(), name='buy-all'),

]
