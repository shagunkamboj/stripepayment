# urls.py

# from django.urls import path
# from .views import PaymentIntentView
# from django.contrib import admin
# from django.urls import path,include

# urlpatterns = [
#      path('admin/', admin.site.urls),
#     path('payment/', PaymentIntentView.as_view()),
# ]
from payment.views import StripeIntentView, CustomPaymentView,CreateSubscriptionView,StripeWebhookView
from django.urls import path,include
from django.contrib import admin
urlpatterns = [


path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
path('custom-payment/', CustomPaymentView.as_view(), name='custom-payment'),
path('create-subscription/', CreateSubscriptionView.as_view(), name='create_subscription'),
path('stripe-webhook/', StripeWebhookView.as_view(), name='stripe_webhook'),
]