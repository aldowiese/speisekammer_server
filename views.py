from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Product, ProductInstance
from .serializers import ProductSerializer, InstanceSerializer, ItemCountSerializer

from django.views.generic.base import TemplateView

class ProductListView(APIView):
    def get(self, request):
        if 'filter' in request.query_params:
            products = Product.objects.filter(name__contains=request.query_params['filter'])
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            if not Product.objects.filter(name=request.data['name']).exists():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductView(APIView):
    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_product(pk)
        serializer = ProductSerializer(product) 
        return Response(serializer.data)

class InstanceListView(APIView):
    def get(self, request):
        instances = ProductInstance.objects.all()
        serializer = InstanceSerializer(instances, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InstanceSerializer(data=request.data)
        if serializer.is_valid():
            if not ProductInstance.objects.filter(barcode=request.data['barcode']).exists():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_instance(barcode):
    try:
        return ProductInstance.objects.get(barcode=barcode)
    except ProductInstance.DoesNotExist:
        raise Http404

def productio(barcode, io):
    instance = get_instance(barcode)
    instance.item_count += io
    if instance.item_count < 0:
        instance.item_count = 0
    instance.save()
    return instance

class InstanceView(APIView):
    def get(self, request, barcode):
        instance = get_instance(barcode)
        serializer = InstanceSerializer(instance)
        return Response(serializer.data)

class ItemCountView(APIView):
    def get(self, request, barcode):
        instance = get_instance(barcode)
        serializer = ItemCountSerializer(instance)
        return Response(serializer.data)

    def put(self, request, barcode):
        instance = productio(barcode, 1)
        serializer = ItemCountSerializer(instance)
        return Response(serializer.data)

    def delete(self, request, barcode):
        instance = productio(barcode, -1)
        serializer = ItemCountSerializer(instance)
        return Response(serializer.data)

class IndexView(TemplateView):
    template_name = 'speisekammer_server/index.html'

class SpeisekammerView(TemplateView):
    template_name = 'speisekammer_server/speisekammer_list.html'

    def get_context_data(self, **kwargs):
        context = super(SpeisekammerView, self).get_context_data(**kwargs)
        if 'filter' in self.request.GET:
            products = Product.objects.filter(name__contains=self.request.GET['filter'])
        else:
            products = Product.objects.all()
        for p in products:
            instances = ProductInstance.objects.filter(product=p.id)
            count_sum = sum([i.item_count for i in instances])
            p.count_sum = count_sum
        context.update({'products':products})
        return context

class SpeisekammerProductView(TemplateView):
    template_name = 'speisekammer_server/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SpeisekammerProductView, self).get_context_data(**kwargs)
        context.update({
            'product':Product.objects.get(id=self.kwargs['pk']),
            'instances':ProductInstance.objects.filter(product=self.kwargs['pk'])
        })
        return context
