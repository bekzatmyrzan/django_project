from django.shortcuts import render
from django.http import HttpResponse
from django.urls import  include
from django.http import HttpResponseRedirect, JsonResponse
from . import templates
from ecomapp.models import Category,Product,CartItem,Cart, Order # # TODO: Order
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth import login, authenticate # # TODO: Order
from ecomapp.forms import OrderForm, RegistrationForm, LoginForm # # TODO: Order
from django.views.generic import View # # TODO: Order
from django.contrib.auth.models import User # # TODO: Order

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


    popular_products = Product.objects.filter(numberOfClicks__gt=3).order_by('-numberOfClicks')[:3]
    categories = Category.objects.all()
    products = Product.objects.all()

    context = {
        'cart':cart,
        'popular_products':popular_products,
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
    product.numberOfClicks = product.numberOfClicks + 1
    product.save()
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
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total+=round(float(item.item_total))
    cart.cart_total = new_cart_total
    cart.save()

    return JsonResponse({ 'cart_total': cart.items.count(),
    'cart_total_price':cart.cart_total})

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
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total+=round(float(item.item_total))
    cart.cart_total = new_cart_total
    cart.save()

    return JsonResponse({ 'cart_total': cart.items.count(),
    'cart_total_price':cart.cart_total})

def change_item_qty(request):
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

    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart_item = CartItem.objects.get(id = int(item_id))
    cart_item.qty = int(qty)
    cart_item.item_total = round(float(qty))*round(float(cart_item.product.price))
    cart_item.save()
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total+=round(float(item.item_total))
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse({'cart_total':cart.items.count(),
        'item_total':cart_item.item_total,
        'cart_total_price':cart.cart_total})

def checkout_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	categories = Category.objects.all()
	context = {
		'cart': cart,
		'categories': categories
	}
	return render(request, 'checkout.html', context)



def order_create_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	form = OrderForm(request.POST or None)
	categories = Category.objects.all()
	context = {
		'form': form,
		'cart': cart,
		'categories': categories
	}
	return render(request, 'order.html', context)


def make_order_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	form = OrderForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		name = form.cleaned_data['name']
		last_name = form.cleaned_data['last_name']
		phone = form.cleaned_data['phone']
		buying_type = form.cleaned_data['buying_type']
		address = form.cleaned_data['address']
		comments = form.cleaned_data['comments']
		new_order = Order.objects.create(
			user=request.user,
			items=cart,
			total=cart.cart_total,
			first_name=name,
			last_name=last_name,
			phone=phone,
			address=address,
			buying_type=buying_type,
			comments=comments
			)
		del request.session['cart_id']
		del request.session['total']
		return HttpResponseRedirect(reverse('thank_you'))
	return render(request, 'order.html', {'categories': categories})

def account_view(request):
	order = Order.objects.filter(user=request.user).order_by('-id')
	categories = Category.objects.all()
	for item in order:
		for new_item in item.items.items.all():
			print(new_item.item_total)
	context = {
		'order': order,
		'categories': categories
	}
	return render(request, 'account.html', context)

def registration_view(request):
	form = RegistrationForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		new_user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		email = form.cleaned_data['email']
		first_name = form.cleaned_data['first_name']
		last_name = form.cleaned_data['last_name']
		new_user.username = username
		new_user.set_password(password)
		new_user.first_name = first_name
		new_user.last_name = last_name
		new_user.email = email
		new_user.save()
		login_user = authenticate(username=username, password=password)
		if login_user:
			login(request, login_user)
			return HttpResponseRedirect(reverse('base'))
	context = {
		'form': form,
		'categories': categories
	}
	return render(request, 'registration.html', context)


def login_view(request):
	form = LoginForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		login_user = authenticate(username=username, password=password)
		if login_user:
			login(request, login_user)
			return HttpResponseRedirect(reverse('base'))
	context = {
		'form': form,
		'categories': categories
	}
	return render(request, 'login.html', context)

def search_view(request):
    try:
        if request.method=="POST":
            text_for_search = request.POST.get("search_field")
            if len(text_for_search)>0:
                search_res = Product.objects.filter(description__contains=text_for_search)
            return render(request, "search.html",
                        {"search_res":search_res,"empty_res":"There is no product"})
    except:
        return render(request, "search.html",{"empty_res":"There is no product"})

def sort_by_price_increase_view(request,category_slug):
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
    products_of_category = Product.objects.filter(category = category).order_by('price')
    categories = Category.objects.all()
    context ={
        'cart':cart,
        'category':category,
        'categories' : categories,
        'products_of_category':products_of_category
    }
    return render(request,'category.html',context)


def sort_by_price_decrease_view(request,category_slug):
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
    products_of_category = Product.objects.filter(category = category).order_by('-price')
    categories = Category.objects.all()
    context ={
        'cart':cart,
        'category':category,
        'categories' : categories,
        'products_of_category':products_of_category
    }
    return render(request,'category.html',context)
