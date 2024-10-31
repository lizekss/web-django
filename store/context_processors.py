from store.models import Category


def categories(request):
    categories = Category.objects.all()
    return {
        'all_categories': categories,
    }
