from .cart import Cart

def cart(request):
    context = {}

    context['cart'] = Cart(request)

    return context