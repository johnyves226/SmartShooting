import stripe
from django.template import loader
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from .form import OrderItemForm, Order, MyOrderForm, MyOrderItemForm

from .models import Order, OrderItem


def checkout(request):
    if request.method == 'POST':
        form = OrderItemForm(data=request.POST)
    pass
    # if serializer.is_valid():
    #     stripe.api_key = settings.STRIPE_SECRET_KEY
    #     paid_amount = sum(
    #         item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
    #
    #     try:
    #         charge = stripe.Charge.create(
    #             amount=int(paid_amount * 100),
    #             currency='USD',
    #             description='Charge from Djackets',
    #             source=serializer.validated_data['stripe_token']
    #         )
    #
    #         serializer.save(user=request.user, paid_amount=paid_amount)
    #
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except Exception:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersList(APIView):
    pass
    # def get(self, request, format=None):
    #     template = loader.get_template('../templates/showImage.html')
    #     orders = Order.objects.filter(user=request.user)
    #     serializer = MyOrderSerializer(orders, many=True)
    #     return Response(serializer.data)
