from django import template
from store.models import Category

register = template.Library()


@register.inclusion_tag('core/menu.html')
def menu():
    #context = {}
    categories = Category.objects.all()

    #context['categories'] = categories
    return {'categories': categories}
