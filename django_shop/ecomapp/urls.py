from django.conf.urls import url
from django.urls import path, include
from . import views
from ecomapp.views import base_view,product_view,category_view

urlpatterns = [
    url(r'^categories/(?P<category_slug>[\w-]+)/$', category_view, name='category_detail'),
    url(r'^products/(?P<product_slug>[\w-]+)/$', product_view, name='product_detail'),
    # path('category/<str:category_slug>', category_view,name = 'category_detail'),
    # path('product/<str:product_slug>', product_view,name = 'product_detail'),
    url(r'^$', base_view,name = 'base'),
]
