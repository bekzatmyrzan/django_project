from django.shortcuts import render
from django.http import HttpResponse
from django.urls import  include
from . import templates
from ecomapp.models import Category,Product



def base_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories' : categories,
        'products' : products
    }
    return render(request,'base.html',context)

def product_view(request,product_slug):
    product = Product.objects.get(slug = product_slug)
    context ={
        'product':product
    }
    return render(request,'product.html',context)

def category_view(request,category_slug):
    category = Category.objects.get(slug = category_slug)
    context ={
        'category':category
    }
    return render(request,'category.html',context)
