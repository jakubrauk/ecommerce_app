def create_groups_permissions(sender, **kwargs):
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Group, Permission
    from base_app.models import Product, ProductCategory, Order, OrderItem, OrderAddress
    salesman_group, salesman_group_created = Group.objects.get_or_create(name='Salesman')
    customer_group, customer_group_created = Group.objects.get_or_create(name='Customer')

    if salesman_group_created:
        print('Salesman group created')

    if customer_group_created:
        print('Customer group created')

    full_access = ['add', 'view', 'change', 'delete']

    # (ModelClass, [{model}_action])
    SALESMAN_PERMISSIONS = [
        (Product, full_access),
        (ProductCategory, full_access),
        (Order, ['view']),
        (OrderItem, ['view']),
        (OrderAddress, ['view'])
    ]

    CUSTOMER_PERMISSIONS = [
        (ProductCategory, ['view']),
        (Order, ['add']),
        (OrderItem, ['add']),
        (OrderAddress, ['add'])
    ]

    for group, permissions in zip([salesman_group, customer_group], [SALESMAN_PERMISSIONS, CUSTOMER_PERMISSIONS]):
        group_permissions = group.permissions.all()
        for model_class, actions in permissions:
            ct = ContentType.objects.get_for_model(model_class)
            for action in actions:
                perm = Permission.objects.get(content_type=ct, codename=action+'_'+ct.model)
                if perm not in group_permissions:
                    group.permissions.add(perm)
