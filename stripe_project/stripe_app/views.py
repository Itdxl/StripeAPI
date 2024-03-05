import stripe 



from django.shortcuts import get_object_or_404, render
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item


class ItemView(APIView):

    def get(self, request, pk):
        public_stripe_key = settings.PUBLIC_STRIPE_KEY
        item = get_object_or_404(Item, pk=pk)
        context = {
            'item': item,
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