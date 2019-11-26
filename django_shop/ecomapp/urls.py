from django.conf.urls import url
from django.urls import path, include
from . import views
from ecomapp.views import base_view,product_view,category_view,cart_view,add_to_cart_view,remove_from_cart_view

urlpatterns = [
    url(r'^categories/(?P<category_slug>[\w-]+)/$', category_view, name='category_detail'),
    url(r'^products/(?P<product_slug>[\w-]+)/$', product_view, name='product_detail'),
    url(r'^cart/$',cart_view, name = 'cart'),
    url(r'^add_to_cart/$',add_to_cart_view,name = 'add_to_cart'),
    url(r'^remove_from_cart/$',remove_from_cart_view,name = 'remove_from_cart'),
    # path('category/<str:category_slug>', category_view,name = 'category_detail'),
    # path('product/<str:product_slug>', product_view,name = 'product_detail'),
    url(r'^$', base_view,name = 'base'),
]
