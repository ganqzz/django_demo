from rest_framework.fields import (
    IntegerField, BooleanField, FloatField, CharField, DecimalField,
    DateTimeField, ImageField, FileField, DictField, ListField
)
from rest_framework.serializers import ModelSerializer, Serializer

from store.models import Product, Order


class OrderSerializer(ModelSerializer):
    quantity = IntegerField(min_value=1, max_value=100)

    class Meta:
        model = Order
        fields = ('product', 'quantity')


class ProductSerializer(ModelSerializer):
    is_on_sale = BooleanField(read_only=True)
    current_price = FloatField(read_only=True)
    description = CharField(min_length=2, max_length=200)
    cart_items = OrderSerializer(many=True, read_only=True)
    # price = FloatField(min_value=1.00, max_value=100000)
    price = DecimalField(
        min_value=1.00, max_value=100000,
        max_digits=None, decimal_places=2,
    )
    sale_start = DateTimeField(
        required=False,
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
        help_text='Accepted format is "12:01 PM 16 April 2019"',
        style={'input_type': 'text', 'placeholder': '12:01 AM 28 July 2019'},
    )
    sale_end = DateTimeField(
        required=False,
        input_formats=['%I:%M %p %d %B %Y'], format=None, allow_null=True,
        help_text='Accepted format is "12:01 PM 16 April 2019"',
        style={'input_type': 'text', 'placeholder': '12:01 AM 28 July 2019'},
    )
    photo = ImageField(default=None)
    warranty = FileField(write_only=True, default=None)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'price', 'sale_start', 'sale_end',
            'is_on_sale', 'current_price', 'cart_items',
            'photo', 'warranty',
        )

    def update(self, instance, validated_data):
        if validated_data.get('warranty', None):
            instance.description += '\n\nWarranty Information:\n'
            instance.description += b'; '.join(
                validated_data['warranty'].readlines()
            ).decode('utf-8')
        return super().update(instance, validated_data)

    def create(self, validated_data):
        validated_data.pop('warranty')  # remove
        return Product.objects.create(**validated_data)


class ProductStatSerializer(Serializer):
    """
    Not combined to a specific model
    Read only, no create or update
    """
    stats = DictField(
        child=ListField(
            child=IntegerField(),
        )
    )
