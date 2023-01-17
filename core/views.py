from django.contrib import messages
from django.shortcuts import render, redirect

from store.models import Product, Category
from userprofile.models import UserProfile
from userprofile.forms import DepartmentForm


# Create your views here.
def frontpage(request):
    global products
    context = {}

    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            products = Product.objects.filter(status=Product.DISPONIBLE).filter(departamento__exact=form['title'].value())
    else:
        form = DepartmentForm()
        products = Product.objects.filter(status=Product.DISPONIBLE)

    categories = Category.objects.all()

    context['categories'] = categories
    context['form'] = form
    context['products'] = products

    return render(request, 'core/frontpage.html', context)


def about(request):
    context = {}
    return render(request, 'core/about.html', context)
