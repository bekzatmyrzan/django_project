from django.contrib import admin
from ecomapp.models import Category
from ecomapp.models import Brand
from ecomapp.models import Product
from ecomapp.models import CartItem
from ecomapp.models import Cart

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
# Register your models here.
