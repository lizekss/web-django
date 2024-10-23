from django.core.paginator import Paginator
from django.db.models import ExpressionWrapper, DecimalField, F, Max, Min, Avg, Sum, Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from store.models import Product, Category


def product_list(request):
    products = Product.objects.prefetch_related('categories')
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


def category_list(request):
    top_level_categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'old/category_list.html', {'categories': top_level_categories})


def category_detail(request, category_id):
    category = get_object_or_404(Category.objects, id=category_id)

    subcategories = category.get_descendants(include_self=True)

    products = Product.objects.filter(categories__in=subcategories).distinct().annotate(
        total_stock_value=ExpressionWrapper(
            F('price') * F('quantity'),
            output_field=DecimalField(max_digits=20, decimal_places=2)
        )
    )

    stats = products.aggregate(
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price'),
        total_value=Sum(
            ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField(max_digits=20, decimal_places=2)))
    )

    return render(request, 'old/category_detail.html', {
        'category': category,
        'products': products,
        'stats': stats
    })


def category_listing(request, slug=None):
    query = request.GET.get('q')
    products = Product.objects.prefetch_related('categories')

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    categories_list = Category.objects.filter(parent__isnull=True)

    if slug:
        category = get_object_or_404(Category, slug=slug)
        subcategories = category.get_descendants(include_self=True)
        categories_list = subcategories.exclude(id=category.id)
        products = products.filter(categories__in=subcategories).distinct()

    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Shop',
        'products': page_obj,
        'categories': categories_list,
    }

    return render(request, 'shop.html', context)


def contact(request):
    return render(request, 'contact.html', {'title': 'Contact'})


def product_detail(request, slug):
    return render(request, 'shop-detail.html', {'title': 'Shop Detail'})


def index(request):
    return render(request, 'index.html', {'title': 'Home'})
