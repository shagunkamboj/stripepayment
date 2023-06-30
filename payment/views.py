# import stripe
# import pdb
# from rest_framework.views import APIView
# from rest_framework.response import Response

# stripe.api_key = 'sk_test_51NKwuYSErS4Hkbpk3Nh4Lvv0nrkykCJOaWJy8qAXmdudVjDQIoKVQaq5KZAgfkzP55Vnou2ZWnEPkZSQAF7mHjcG00ZFF1tCov'

# class PaymentIntentView(APIView):
#     def post(self, request, format=None):
#         try:
#             # Retrieve the necessary data from the request
#             items = request.data.get('items')
#             description = request.data.get('description')
#             # import pdb;
#             # pdb.set_trace()
#             # Calculate the order amount dynamically based on items
#             total_amount = self.calculate_order_amount(items)

#             # Create a PaymentIntent with the order amount, currency, and description
#             intent = stripe.PaymentIntent.create(
#                 amount=int(total_amount * 100),  # Convert amount to paise
#                 currency='inr',
#                 description=description,
#                 payment_method_types=['card'],
                
               
               
                
#             )

#             # Return the client secret and total amount of the payment intent
#             return Response({'clientSecret': intent.client_secret, 'amount': total_amount,'description':description,'items':items})
#         except Exception as e:
#             return Response({'error': str(e)}, status=403)

    
#     def calculate_order_amount(self, items):
#         total_amount = 0

#         if items is not None:
#             for item in items:
#                 price = float(item.get('price', 0))
#                 quantity = int(item.get('quantity', 1))  # Default quantity is 1 if not specified
#                 total_amount += price * quantity

#         return total_amount




import json
from django.http import JsonResponse
from django.views import View
import stripe
from .models import Price
from django.conf import settings
from django.views.generic import TemplateView
from .models import Product, Price
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
import os

stripe.api_key = 'sk_test_51NKwuYSErS4Hkbpk3Nh4Lvv0nrkykCJOaWJy8qAXmdudVjDQIoKVQaq5KZAgfkzP55Vnou2ZWnEPkZSQAF7mHjcG00ZFF1tCov'
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
           
            req_json = json.loads(request.body)
            description = req_json.get('description',"")
            
            customer = stripe.Customer.create(email=req_json['email'])
            price = Price.objects.get(id=self.kwargs["pk"])
            
            print(price)
            intent = stripe.PaymentIntent.create(
                amount=price.price,
                currency='inr',
                customer=customer['id'],
                description=description,
                
                metadata={
                    "price_id": price.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret'],'price':price.price
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


class CustomPaymentView(TemplateView):
    template_name = "custom_payment.html"
    

    def get_context_data(self, **kwargs):
        
        
        product = Product.objects.get(name="watch")
        prices = Price.objects.filter(product=product)
        context = super().get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices,
            "STRIPE_PUBLIC_KEY": "pk_test_51NKwuYSErS4Hkbpk7ogRr6X40o6vDXwaw9TtDkZ1A1xQfMlxfTWJxDP4mNDlsVMQlA3iR0N4YHwzi1m4TrGeGxB700nGJRbMnf"
        })
        
        return context




class CreateSubscriptionView(APIView):
    def post(self, request):
        customer_email = request.data.get('email')
        customer_name = request.data.get('name')
        price_id = request.data.get('priceId')
        #webhook_secret = os.getenv('whsec_6807a9595e33b655d659af60879750d1ad6324480cecbb7bff068f6240597543')

        try:
            customer = stripe.Customer.create(
                email=customer_email,
                name=customer_name,
                address={
                    'city': 'Brothers',
                    'country': 'US',
                    'line1': '27 Fredrick Ave',
                    'postal_code': '97712',
                    'state': 'CA',
                },
                shipping={
                    'name': customer_name,
                    'address': {
                        'city': 'Brothers',
                        'country': 'US',
                        'line1': '27 Fredrick Ave',
                        'postal_code': '97712',
                        'state': 'CA',
                    },
                }
            )

            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{
                    'price': price_id,
                }],
                payment_behavior='default_incomplete',
                payment_settings={'save_default_payment_method': 'on_subscription'},
                expand=['latest_invoice.payment_intent'],
            )

            return Response({
                'subscriptionId': subscription.id,
                'clientSecret': subscription.latest_invoice.payment_intent.client_secret,
            })

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=400)
import json

class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        webhook_secret = os.getenv('whsec_6807a9595e33b655d659af60879750d1ad6324480cecbb7bff068f6240597543')

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
            data = event['data']
            event_type = event['type']

            if event_type == 'invoice.paid':
                # Handle the 'invoice.paid' event
                pass

            elif event_type == 'invoice.payment_failed':
                # Handle the 'invoice.payment_failed' event
                pass

            elif event_type == 'customer.subscription.deleted':
                # Handle the 'customer.subscription.deleted' event
                pass

            return Response({'status': 'success'})

        except (ValueError, stripe.error.SignatureVerificationError) as e:
            return Response({'error': str(e)}, status=400)
