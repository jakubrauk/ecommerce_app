from datetime import datetime, timedelta

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from base_app.models import ProductCategory, Product, OrderAddress, Order, OrderItem


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    thumbnail = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = ['url', 'name', 'description', 'price', 'category', 'picture', 'thumbnail']

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        product.create_thumbnail()
        return product


class ProductStatisticsSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    sum_ordered = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['product', 'sum_ordered']

    def get_product(self, obj):
        instance = Product.objects.get(id=obj['product'])
        return ProductSerializer(instance=instance, context={'request': self._context['request']}).data


class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['url', 'name', 'products']


class OrderAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderAddress
        fields = ['url', 'street', 'house_number', 'flat_number', 'city', 'postal_code']


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    order = serializers.HyperlinkedRelatedField(view_name='order-detail', read_only=True)
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderItem
        fields = ['url', 'product', 'amount', 'order']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    items = OrderItemSerializer(many=True)
    address = OrderAddressSerializer(many=False)
    total_price = serializers.ReadOnlyField()
    payment_date = serializers.ReadOnlyField()
    order_date = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['url', 'customer', 'payment_date', 'order_date', 'total_price', 'address', 'items']

    def create(self, validated_data):
        items = validated_data.pop('items')
        address = validated_data.pop('address')
        address_instance = OrderAddress.objects.create(**address)
        order_date = datetime.now().date()
        payment_date = order_date + timedelta(days=5)
        total_price = sum([item['product'].price * item['amount'] for item in items])
        order = Order.objects.create(
            address=address_instance,
            order_date=order_date,
            payment_date=payment_date,
            total_price=total_price,
            **validated_data
        )
        for item in items:
            OrderItem.objects.create(order=order, **item)
        return order
