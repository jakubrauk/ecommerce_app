"""
URL configuration for ecommerce_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from base_app import views
from ecommerce_project import settings

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'products_statistics', views.ProductsStatistics, basename='productsstatistics')
router.register(r'categories', views.ProductCategoryViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'orderaddresses', views.OrderAddressViewSet, basename='orderaddress')
router.register(r'orderitems', views.OrderItemViewSet, basename='orderitem')


urlpatterns = [
    path('', include(router.urls)),
    # path('product_statistics/', views.ProductsStatistics.as_view({'get': 'list'}), name='product-statistics'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
