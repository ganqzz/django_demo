import operator
from functools import reduce

from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from store.models import Product
from store.serializers import ProductSerializer, ProductStatSerializer


def index(request):
    context = {'products': Product.objects.all()}
    return render(request, 'store/product_list.html', context)


def show(request, pk):
    product = Product.objects.prefetch_related('orders').get(pk=pk)
    total_orders = reduce(operator.add, (o.quantity for o in product.orders.all()))
    context = {'product': product, 'total_orders': total_orders}
    return render(request, 'store/product.html', context)


# --- API ---


class ProductsPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 100


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id',)
    search_fields = ('name', 'description')
    pagination_class = ProductsPagination

    def get_queryset(self):
        on_sale = self.request.query_params.get('on_sale', None)
        if on_sale is None:
            return super().get_queryset()
        queryset = Product.objects.all()
        if on_sale.lower() == 'true':
            from django.utils import timezone
            now = timezone.now()
            return queryset.filter(
                sale_start__lte=now,
                sale_end__gte=now,
            )
        return queryset


class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get('price')
            if price is not None and float(price) <= 0.0:
                raise ValidationError({'price': 'Must be above $0.00'})
        except ValueError:
            raise ValidationError({'price': 'A valid number is required'})
        return super().create(request, *args, **kwargs)


class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """GET, PUT/PATCH, DELETE"""
    queryset = Product.objects.all()
    lookup_field = 'pk'
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('product_data_{}'.format(product_id))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            product = response.data
            cache.set('product_data_{}'.format(product['id']), {
                'name': product['name'],
                'description': product['description'],
                'price': product['price'],
            })
        return response


# demo?????????????????????APIView
class ProductStats(GenericAPIView):
    lookup_field = 'pk'  # lookup_url_kwarg
    serializer_class = ProductStatSerializer
    queryset = Product.objects.all()

    def get(self, request, id, format=None):
        product = self.get_object()
        # ???????????????????????????1-1???????????????????????????????????????composite field
        serializer = ProductStatSerializer({
            'stats': {
                '2019-01-01': [5, 10, 15],
                '2019-01-02': [20, 1, 1],
            }
        })
        return Response(serializer.data)
