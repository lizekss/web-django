from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from store.models import Product, Category


def product_list(request):
    products = Product.objects.all()
    data = []
    for product in products:
        categories = product.categories.all()
        categories_list = [{'id': cat.id, 'name': cat.name}
                           for cat in categories]
        data.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'categories': categories_list,
            'image': product.image.url if product.image else None
        })
    return JsonResponse(data, safe=False)


def product_detail(request):
    return HttpResponse("This is the product detail.")


def category_list(request):
    categories = Category.objects.all()
    data = []
    for category in categories:
        data.append({
            'id': category.id,
            'name': category.name,
            'parent': category.parent.name if category.parent else None
        })
    return JsonResponse(data, safe=False)
