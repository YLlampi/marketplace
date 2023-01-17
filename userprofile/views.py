from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify

from .models import UserProfile
from .forms import CustomUserCreationForm, CustomUserForm
from store.forms import ProductForm

from store.models import Product, OrderItem, Order
from .departamentos import DEPARTAMENTOS_CHOICES


# Create your views here.
def vendor_detail(request, pk):
    context = {}
    user = User.objects.get(pk=pk)
    context['user'] = user

    products = user.products.filter(status=Product.DISPONIBLE)
    context['products'] = products

    return render(request, 'userprofile/vendor_detail.html', context)


def my_func_order(item):
    return item.order.id

@login_required
def my_store(request):
    context = {}

    # products = request.user.products.exclude(status=Product.DELETED)
    products = request.user.products.all()
    context['products'] = products

    #order_item.order.id
    order_items = list(OrderItem.objects.filter(product__user=request.user))
    order_items.sort(reverse=True, key=my_func_order)
    context['order_items'] = order_items

    total_price = 0
    for i in range(len(order_items)):
        total_price += order_items[i].get_display_price() * order_items[i].quantity
    context['total_price'] = total_price

    return render(request, 'userprofile/my_store.html', context)


@login_required
def my_store_order_detail(request, pk):
    context = {}

    order = get_object_or_404(Order, pk=pk)
    context['order'] = order

    total_price = 0
    for item in order.items.all():
        if item.product.user == request.user:
            total_price += item.get_display_price()
    context['total_price'] = total_price

    return render(request, 'userprofile/my_store_order_detail.html', context)


@login_required
def add_product(request):
    context = {}

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        user = UserProfile.objects.get(user=request.user)

        if form.is_valid():
            title = request.POST.get('title')

            product = form.save(commit=False)
            product.user = request.user
            product.departamento = user.departamento
            product.slug = slugify(title)
            product.save()

            messages.success(request, 'The product was added')

            return redirect('my_store')
    else:
        form = ProductForm()

    context['form'] = form
    context['title'] = 'Add product'

    return render(request, 'userprofile/product_form.html', context)


@login_required
def edit_product(request, pk):
    context = {}

    product = Product.objects.filter(user=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            ###
            #product.thumbnail = None
            #product.get_thumbnail()
            ##
            form.save()

            messages.success(request, 'The changes was saved')

            return redirect('my_store')
    else:
        form = ProductForm(instance=product)

    context['form'] = form
    context['title'] = 'Edit product'
    context['product'] = product

    return render(request, 'userprofile/product_form.html', context)


@login_required
def delete_product(request, pk):
    context = {}

    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED

    product.save()

    messages.success(request, 'The product was deleted')

    return redirect('my_store')


@login_required
def myaccount(request):
    context = {}

    user = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)

        if not user.first_name or not user.last_name or not user.num_whatsapp:
            messages.error(request, 'Actualizar datos para poder continuar...')
            return redirect('myaccount')

        if form.is_valid():
            user.user.first_name = user.first_name
            user.user.last_name = user.last_name
            user.user.save()

            user.is_vendor = True

            form.save()

            messages.success(request, 'Ahora puedes vender productos...')

            return redirect('my_store')
    else:
        form = CustomUserForm(instance=user)

    context['form'] = form
    context['user'] = user

    return render(request, 'userprofile/myaccount.html', context)

@login_required
def edit_account(request, pk):
    context = {}

    user = UserProfile.objects.get(id=pk)

    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            user.user.first_name = user.first_name
            user.user.last_name = user.last_name
            user.user.save()
            form.save()

            messages.success(request, 'The changes was saved')

            return redirect('my_store')
    else:
        form = CustomUserForm(instance=user)

    context['form'] = form
    context['title'] = 'Edit account'
    context['user'] = user

    return render(request, 'userprofile/account_form.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            userprofile = UserProfile.objects.create(user=user)

            return redirect('frontpage')

    else:
        form = CustomUserCreationForm()

    context['form'] = form

    return render(request, 'userprofile/signup.html', context)
