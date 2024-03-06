import stripe 

from django.db.models import Sum, F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item, Order, OrderItem
from .serializers import OrderItemSerializer


class OrderView(APIView):
    def get(self, request):
        order, created = Order.objects.get_or_create()
        order_items = OrderItem.objects.filter(order=order)
        # берем queryset order_items
        # делаем новое поле total_for_item и через anotate считаем общую цену
        # anotate для каждого элемента(позиции) заказа
        # aggregate считает общую сумму всех СУММ ПОЗИЦИЙ
        # F используется для обращения к значениям полей
        total = order_items.annotate(total_for_item=F('price') * F('quantity')) \
                           .aggregate(total=Sum('total_for_item'))['total']

        serializer = OrderItemSerializer(order_items, many=True)
        data = {
            'order_items': serializer.data,
            'total': total if total else 0
        }
        return Response(data, status=status.HTTP_200_OK)
    

    def post(self, request, item_id):
        item = get_object_or_404(Item, pk=item_id)
        # Проверяем или создаем. (user=request.user), если делать пользователей
        order_instance, created = Order.objects.get_or_create()
        price = item.price
        order_item_instance, created = OrderItem.objects.get_or_create(order=order_instance, item=item, price=price)
        if not created:
            order_item_instance.quantity += 1
            order_item_instance.save()
        
        return Response({'message': 'Added to order'})
    

class ItemView(APIView):
    def get(self, request, pk):
        public_stripe_key = settings.PUBLIC_STRIPE_KEY
        item = get_object_or_404(Item, pk=pk)
        context = {
            'item': item,
            'public_stripe_key': public_stripe_key
        }
        return render(request, 'item_details.html', context)

stripe.api_key = settings.STRIPE_SECRET_KEY
def create_stripe_session(amount):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Purchase",  # Название товара или заказа
                    },
                    "unit_amount": int(amount * 100),  # Сумма в копейках
                },
                "quantity": 1,
            }],
            mode='payment',
            success_url=settings.REDIRECT_DOMAIN + '/success',
            cancel_url=settings.REDIRECT_DOMAIN + '/cancel',
        )
        return session.id
    except Exception as e:
        # Обработка ошибок создания сессии оплаты
        return str(e)

   
class BuyItemView(APIView):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        session_id = create_stripe_session(item.price)
        return Response({'session_id': session_id})
    
class BuyOrderView(APIView):
     def get(self, request):
        order, created = Order.objects.get_or_create()
        order_items = OrderItem.objects.filter(order=order)
        total = order_items.annotate(total_for_item=F('price') * F('quantity')) \
                           .aggregate(total=Sum('total_for_item'))['total']
        session_id = create_stripe_session(total)
        return Response({'session_id': session_id})

# class BuyItemView(APIView):
#     def get(self, request, pk):
#         item = get_object_or_404(Item, pk=pk)
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         # Создание сессии оплаты Stripe
#         try:
#             session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=[{
#                     "price_data": {
#                         "currency": "eur",
#                         "product_data": {
#                         "name": item.name,
#                     },
#                     # Stripe не работает с десятичными числами
#                     "unit_amount": int(item.price* 100),
#                 },
#                     "quantity": 1,
#                 }],
#                 mode='payment',
#                 success_url = settings.REDIRECT_DOMAIN + '/success',
# 			    cancel_url = settings.REDIRECT_DOMAIN + '/cancel',
#             )
            
#             # Возвращаем идентификатор сессии оплаты
#             return Response({'session_id': session.id})
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

def successful(request):
	return render(request, 'success.html')


def canceled(request):
	return render(request, 'cancel.html')


def get_coupon(self, pk):
        item = get_object_or_404(Item, pk=pk)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            discount = item.discount.get(is_active=True)
        except Exception:
            return None

        coupon = stripe.Coupon.create(
            duration="once",
            id=f"coupon-{item.id}",
            percent_off=discount.amount,
        )
        if coupon:
            return Response({'coupon': coupon.id})
        else:
            return Response({'error': 'Discount not found for item'}, status=status.HTTP_404_NOT_FOUND)

            
        
class CouponView(APIView):
    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY        
        coupons = stripe.Coupon.list()
        coupon_ids = [[coupon.id,coupon.percent_off] for coupon in coupons.data]
        return JsonResponse({'coupons': coupon_ids})

    def delete(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        coupons = stripe.Coupon.list()
        for coupon in coupons.data:
            stripe.Coupon.delete(coupon.id)
        return Response({'message': 'All coupons deleted successfully'})