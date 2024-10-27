from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView


from order.views import AddToCartView
from store.models import Product, Category, Tag


'''
TODO: display alert on out of stock / login required?
sorting on filtered data?
selected input on refresh?
'''


class FilterProductsMixin:
    def filter_products(self, products, request):
        query = request.GET.get('q')
        if query:
            products = products.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        price_range = request.GET.get('priceFilter')
        if price_range:
            products = products.filter(price__lte=price_range)

        sorting = request.GET.get('sorting')
        if sorting == 'price_asc':
            products = products.order_by('price')
        elif sorting == 'price_desc':
            products = products.order_by('-price')

        tag = request.GET.get('tag')
        if tag:
            products = products.filter(tag_id=tag)

        return products


class CategoryListView(FilterProductsMixin, ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        # Base queryset with optimization
        queryset = Product.objects.prefetch_related(
            'categories'
        ).select_related(
            'tag'
        ).order_by('name')

        # Apply filters
        queryset = self.filter_products(queryset, self.request)

        # Filter by category if slug is provided
        slug = self.kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            subcategories = category.get_descendants(include_self=True)
            queryset = queryset.filter(
                categories__in=subcategories
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add additional context
        context['title'] = 'Shop'
        context['tags'] = Tag.objects.all()

        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['existing_params'] = query_params.urlencode()

        # Handle categories based on slug
        slug = self.kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            subcategories = category.get_descendants(include_self=True)
            context['categories'] = subcategories.exclude(id=category.id)
        else:
            context['categories'] = Category.objects.filter(
                parent__isnull=True)

        return context

    def post(self, request, *args, **kwargs):
        """Handle POST requests for adding items to cart"""
        product_id = request.POST.get('product_id')
        if product_id:
            AddToCartView.as_view()(request)
        return self.get(request, *args, **kwargs)


class TitleView(TemplateView):
    """ Basic static view with just the title in context """
    title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class HomeView(TitleView):
    template_name = 'index.html'
    title = 'Home'


class ContactView(TitleView):
    template_name = 'contact.html'
    title = 'Contact'


class ProductDetailView(TitleView):
    """ This should actually extend DetailView, but for now it is static.
     attributes for DetailView: """
    # context_object_name = 'product'
    # model = Product
    template_name = 'shop-detail.html'
    title = 'Shop Detail'

    def get_queryset(self):
        """Optimize the queryset with related data"""
        return super().get_queryset().prefetch_related(
            'categories',
        )
