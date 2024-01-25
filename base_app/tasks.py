from celery import shared_task
from django.core.mail import send_mail


ORDER_ITEMS_TEMPLATE = """
{product_name} - {amount} szt. * {product_price}zł = {product_total_price}zł
"""


CONFIRMATION_EMAIL_TEXT = """
Potwierdzenie zamówienia:
Data złożenia zamówienia: {order_date}
Data płatnośći: {payment_date}
Kwota do zapłaty: {total_price}zł

Adres dostawy:
{customer_first_name} {customer_last_name}
ul. {address_street} {address_house_number} {address_flat_number} {address_city} {address_postal_code}

Zamówione produkty:{order_items}
"""


@shared_task()
def send_order_confirmation_email_task(order_id):
    from base_app.models import Order

    try:
        order = Order.objects.get(id=order_id)
        address = order.address
        items = order.items.all()

        items_text_list = []
        for item in items:
            items_text_list.append(
                ORDER_ITEMS_TEMPLATE.format(**{
                    'product_name': item.product.name,
                    'amount': item.amount,
                    'product_price': "%.2f" % item.product.price,
                    'product_total_price': item.amount * item.product.price
                })
            )

        email_text = CONFIRMATION_EMAIL_TEXT.format(**{
            'order_date': order.order_date.strftime("%d.%m.%Y"),
            'payment_date': order.payment_date.strftime("%d.%m.%Y"),
            'total_price': "%.2f" % order.total_price,
            'customer_first_name': order.customer.first_name,
            'customer_last_name': order.customer.last_name,
            'address_street': address.street,
            'address_house_number': address.house_number,
            'address_flat_number': address.flat_number,
            'address_city': address.city,
            'address_postal_code': address.postal_code,
            'order_items': '\n'.join(items_text_list)
        })

        if order.customer.email:
            send_mail(
                "Potwierdzenie złożenia zamówienia",
                email_text,
                "ecommerce@email.com",
                [order.customer.email]
            )
        else:
            print('Failed to send order confirmation email: Customer without email provided')

    except Order.DoesNotExist:
        print('DoesNotExist: Failed to send confirmation email for order', order_id)
