from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from userprofile.forms import DepartmentForm
from .models import Product, Category, Order, OrderItem
from .cart import Cart
from .forms import OrderForm

from userprofile.models import UserProfile


# Create your views here.

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('cart_view')


def change_quantity(request, product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)

    return redirect('cart_view')


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart_view')


def cart_view(request):
    context = {}

    cart = Cart(request)
    context['cart'] = cart

    return render(request, 'store/cart_view.html', context)


@login_required
def checkout(request):
    context = {}

    cart = Cart(request)
    context['cart'] = cart

    user = UserProfile.objects.get(user=request.user)

    mensaje = f'Hola, soy {user.user.username}, quiero comprar los siguientes productos:'
    context['mensaje'] = mensaje

    mensaje_send = mensaje.replace(' ', '%20') + f'%0A'
    context['mensaje_send'] = mensaje_send

    mensaje_2_send = f'%0A%0AQuedo al pendiente para la coordinación de la entrega y el pago del producto%2C muchas gracias.'.replace(
        ' ', '%20')
    context['mensaje_2_send'] = mensaje_2_send

    lista_items = {}
    lista_items_send = {}

    for item in cart:
        product = item['product']
        quantity = int(item['quantity'])
        price = product.price * quantity

        us = UserProfile.objects.get(user=product.user)
        mensaje_s = f'{product.title} x {quantity} = {price}'
        mensaje_s_send = f'%0A{product.title} x {quantity} = {price}'.replace(' ', '%20')

        if not us.num_whatsapp in lista_items:
            lista_items[us.num_whatsapp] = []
        lista_items[us.num_whatsapp].append(mensaje_s)

        if not us.num_whatsapp in lista_items_send:
            lista_items_send[us.num_whatsapp] = ""
        lista_items_send[us.num_whatsapp] += mensaje_s_send

    context['lista_items'] = lista_items
    context['lista_items_send'] = lista_items_send

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            user.user.first_name = form['first_name'].value()
            user.user.last_name = form['last_name'].value()

            user.user.save()

            total_price = 0

            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])

            order = form.save(commit=False)
            order.created_by = request.user

            order.paid_amount = total_price
            order.save()

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

            cart.clear()

            return redirect('myaccount')
    else:
        form = OrderForm()

    context['form'] = form
    return render(request, 'store/checkout.html', context)


def search(request):
    global products
    context = {}

    query = request.GET.get('query', '')

    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            products = Product.objects.filter(status=Product.DISPONIBLE).filter(
                Q(title__icontains=query)
                |
                Q(description__icontains=query)
            ).filter(departamento__exact=form['title'].value())
    else:
        form = DepartmentForm()
        products = Product.objects.filter(status=Product.DISPONIBLE).filter(
            Q(title__icontains=query)
            |
            Q(description__icontains=query)
        )
    context['query'] = query
    context['form'] = form
    context['products'] = products
    return render(request, 'store/search.html', context)


def category_detail(request, slug):
    global products
    context = {}

    category = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            products = category.products.filter(status=Product.DISPONIBLE).filter(
                departamento__exact=form['title'].value())
    else:
        form = DepartmentForm()
        products = category.products.filter(status=Product.DISPONIBLE)

    context['form'] = form
    context['category'] = category
    context['products'] = products

    return render(request, 'store/category_detail.html', context)


def product_detail(request, category_slug, slug):
    context = {}

    product = get_object_or_404(Product, slug=slug, status=Product.DISPONIBLE)
    context['product'] = product

    user_vendor = UserProfile.objects.get(user=product.user)
    context['user_vendor'] = user_vendor

    user = UserProfile.objects.get(user=request.user)

    mensaje = f'Hola {user_vendor.first_name}, soy {user.user.username}, quiero comprar los siguientes productos:'
    context['mensaje'] = mensaje

    mensaje_send = mensaje.replace(' ', '%20') + f'%0A'
    context['mensaje_send'] = mensaje_send


    product_info = f'%0A{product.title} x 1 = S/ {product.get_display_price()}'.replace(' ', '%20')
    context['product_info'] = product_info

    mensaje_2_send = f'%0A%0AQuedo al pendiente para la coordinación de la entrega y el pago del producto%2C muchas gracias.'.replace(
        ' ', '%20')
    context['mensaje_2_send'] = mensaje_2_send



    return render(request, 'store/product_detail.html', context)
