from rest_framework import serializers
from .models import Product, ProductInstance


class InstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductInstance
        fields = ['barcode', 'item_count', 'product']


class ItemCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductInstance
        fields = ['item_count']


class ProductSerializer(serializers.ModelSerializer):
    instances = InstanceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'instances']
