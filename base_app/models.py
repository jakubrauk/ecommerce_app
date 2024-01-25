import os
from io import BytesIO

from django.db import models
from PIL import Image
from django.db.models import Sum


class ProductCategory(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey('ProductCategory', related_name='products', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='pictures')
    thumbnail = models.ImageField(upload_to='thumbnails')

    def __str__(self):
        return f'Product ({self.id}) {self.name}'

    def create_thumbnail(self):
        """
        Creates thumbnail from saved picture. Thumbnail size is max 200x200
        """
        image = Image.open(self.picture.file.file)
        image.thumbnail(size=(200, 200))
        image_file = BytesIO()
        image.save(image_file, image.format)
        name, ext = os.path.splitext(os.path.basename(self.picture.name))
        self.thumbnail.save(name + '_thumbnail' + ext, image_file)


class OrderAddress(models.Model):
    street = models.CharField(max_length=254, blank=True)
    house_number = models.CharField(max_length=254)
    flat_number = models.CharField(max_length=254, blank=True)
    city = models.CharField(max_length=254)
    postal_code = models.CharField(max_length=6)


class Order(models.Model):
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    payment_date = models.DateField()
    order_date = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=2)
    address = models.ForeignKey('OrderAddress', on_delete=models.CASCADE)


class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    amount = models.IntegerField()

    @classmethod
    def get_product_statistics(cls, from_date, to_date, count):
        """
        Returns queryset [{'product': product_id, 'sum_ordered': amount_attr_sum_from_orders}]
        with most frequently ordered products within range [from_date, to_date] of order and
        with specified amount of returned products.
        :param from_date: datetime.date or string Date (YYYY-MM-DD) Lower bound of the order
        :param to_date: datetime.date or string Date (YYYY-MM-DD) Upper bound of the order
        :param count: Products count to be returned
        :return: queryset [{'product': product_id: int, 'sum_ordered': int}]
        """
        return cls.objects.filter(
            order__order_date__gte=from_date,
            order__order_date__lte=to_date,
        ).values('product').annotate(sum_ordered=Sum('amount')).order_by('-sum_ordered')[:count]
