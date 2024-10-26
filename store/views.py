from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView

from order.models import UserCart, CartItem
from store.models import Product, Category, Tag


class AddToCartForm(forms.Form):
    product_id = forms.ModelChoiceField(queryset=Product.objects.all())


class AddToCartView(LoginRequiredMixin, View):
    def _err_out_of_stock(self, request, product):
        messages.error(
            request, f"Only {product.quantity} items available in stock.")

    def post(self, request, *args, **kwargs):
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product_id']

            in_stock = product.quantity >= 1
            if not in_stock:
                self._err_out_of_stock(request, product)
                return

            cart, created = UserCart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product)

            if not created:
                in_stock = cart_item.quantity + 1 >= product.quantity
                if not in_stock:
                    self._err_out_of_stock(request, product)
                    return
                cart_item.quantity += 1

            cart_item.save()


class CategoryListView(ListView):
    """Display and filter products by category"""
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 3

    def _filter_products(self, products):
        """Helper method to filter products based on request parameters"""
        query = self.request.GET.get('q')
        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

        price_range = self.request.GET.get('priceFilter')
        if price_range:
            products = products.filter(price__lte=price_range)

        sorting = self.request.GET.get('sorting')
        if sorting == 'price_asc':
            products = products.order_by('price')
        elif sorting == 'price_desc':
            products = products.order_by('-price')

        tag = self.request.GET.get('tag')
        if tag:
            products = products.filter(tag_id=tag)

        return products

    def get_queryset(self):
        # Base queryset with optimization
        queryset = Product.objects.prefetch_related(
            'categories'
        ).select_related(
            'tag'
        ).order_by('name')

        # Apply filters
        queryset = self._filter_products(queryset)

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


class HomeView(TemplateView):
    """Display the home page"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class ContactView(TemplateView):
    """Display the contact page"""
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact'
        return context


class ProductDetailView(DetailView):
    """Display detailed information about a specific product"""
    model = Product
    template_name = 'shop-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Shop Detail'
        return context

    def get_queryset(self):
        """Optimize the queryset with related data"""
        return super().get_queryset().prefetch_related(
            'categories',
            'tag'
        )
