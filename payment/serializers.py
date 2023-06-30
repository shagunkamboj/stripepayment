# serializers.py
from rest_framework import serializers
from .models import Product

class PaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(decimal_places=2, max_digits=10)
    currency = serializers.CharField(max_length=3)
    source = serializers.CharField()
    description = serializers.CharField(max_length=255)



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'stripe_product_id', 'description', 'image']

