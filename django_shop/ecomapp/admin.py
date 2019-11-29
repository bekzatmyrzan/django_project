from django.contrib import admin
from ecomapp.models import Category
from ecomapp.models import Brand
from ecomapp.models import Product
from ecomapp.models import CartItem
from ecomapp.models import Cart
from ecomapp.models import Order

def make_payed(modeladmin, request, queryset):
    queryset.update(status='Оплачен')
make_payed.short_description = "Пометить как оплаченные"

class OrderAdmin(admin.ModelAdmin):
	list_filter = ['status']
	actions = [make_payed]

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order,OrderAdmin)
# Register your models here.
