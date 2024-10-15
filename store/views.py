from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from store.models import Product, Category


def product_list(request):
    products = Product.objects.all()
    data = []
    for product in products:
        categories = product.categories.all()
        data.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'categories': [cat.name for cat in categories],
            'image': product.image.url if product.image else None
        })
    return JsonResponse(data, safe=False)


def product_detail(request):
    return HttpResponse("This is the product detail.")


def category_list(request):
    top_level_categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'store/category_list.html', {'categories': top_level_categories})


def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)

    # Get all subcategories including the current category
    subcategories = category.get_descendants(include_self=True)

    # Get all products in this category and its subcategories
    products = Product.objects.filter(categories__in=subcategories).distinct()

    return render(request, 'store/category_detail.html', {'category': category, 'products': products})
