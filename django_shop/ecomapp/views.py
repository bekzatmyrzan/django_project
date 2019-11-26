from django.shortcuts import render
from django.http import HttpResponse
from django.urls import  include
from django.http import HttpResponseRedirect, JsonResponse
from . import templates
from ecomapp.models import Category,Product,CartItem,Cart
from django.urls import reverse



def base_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)



    categories = Category.objects.all()
    products = Product.objects.all()

    context = {
        'cart':cart,
        'categories' : categories,
        'products' : products
    }
    return render(request,'base.html',context)

def product_view(request,product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)

    product = Product.objects.get(slug = product_slug)
    categories = Category.objects.all()
    context ={
        'cart':cart,
        'categories' : categories,
        'product':product
    }
    return render(request,'product.html',context)

def category_view(request,category_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)


    category = Category.objects.get(slug = category_slug)
    products_of_category = Product.objects.filter(category = category)
    categories = Category.objects.all()
    context ={
        'cart':cart,
        'category':category,
        'categories' : categories,
        'products_of_category':products_of_category
    }
    return render(request,'category.html',context)

def cart_view(request):
    categories = Category.objects.all()
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)

    context={
        'cart':cart,
        'categories' : categories,
    }
    return render(request,'cart.html',context)

def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    return JsonResponse({ 'cart_total': cart.items.count()})

def remove_from_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id = cart_id)

    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    return JsonResponse({ 'cart_total': cart.items.count()})
