from django.db.models import Sum, F
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe

from .models import Item, Order, OrderItem
from .serializers import OrderItemSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


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





def create_stripe_session(amount):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Order",
                    },
                    "unit_amount": int(amount * 100),  # Stripe не работает с Decimal
                },
                "quantity": 1,
            }],
            mode='payment',
            success_url=settings.REDIRECT_DOMAIN + '/success',
            cancel_url=settings.REDIRECT_DOMAIN + '/cancel',
        )
        return session.id
    except Exception as e:
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


def successful(request):
    return render(request, 'success.html')


def canceled(request):
    return render(request, 'cancel.html')


def index(request):
    return render(request, 'index.html')
