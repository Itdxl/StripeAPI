import stripe 



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
        # Получаем или создаем заказ для текущего пользователя
        order, created = Order.objects.get_or_create()

        # Получаем все элементы заказа для этого заказа
        order_items = OrderItem.objects.filter(order=order)

        # Сериализуем элементы заказа
        serializer = OrderItemSerializer(order_items, many=True)

        # Возвращаем ответ с данными о содержимом корзины
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request, item_id):
        item = get_object_or_404(Item, pk=item_id)
        
        # Проверяем, есть ли корзина у текущего пользователя или создаем новую
        order_instance, created = Order.objects.get_or_create()
        price = item.price

        # Проверяем, есть ли уже такой товар в корзине, и увеличиваем его количество
        order_item_instance, created = OrderItem.objects.get_or_create(order=order_instance, item=item, price=price)
        if not created:
            order_item_instance.quantity += 1
            order_item_instance.save()
        
        return Response({'message': 'Item added to Order successfully'})
    

class ItemView(APIView):

    def get(self, request, pk):
        public_stripe_key = settings.PUBLIC_STRIPE_KEY
        item = get_object_or_404(Item, pk=pk)
        context = {
            'item': item,
            # 'item_id': item.id,
            'public_stripe_key': public_stripe_key
        }
        return render(request, 'item_details.html', context)



class BuyItemView(APIView):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        # item_id = self.kwargs['pk']
        # item = get_object_or_404(Item, pk=item_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Создание сессии оплаты Stripe
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                        "name": item.name,
                    },
                    "unit_amount": int(item.price* 100),
                },
                    "quantity": 1,
                }],
                mode='payment',
                success_url = settings.REDIRECT_DOMAIN + '/success',
			    cancel_url = settings.REDIRECT_DOMAIN + '/cancel',
            )
            
            # Возвращаем идентификатор сессии оплаты
            return Response({'session_id': session.id})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

def successful(request):
	return render(request, 'success.html')


def canceled(request):
	return render(request, 'cancel.html')