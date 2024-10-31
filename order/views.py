from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from order.models import UserCart, CartItem
from store.models import Product


class CartView(LoginRequiredMixin, TemplateView):
    login_url = '/store/login/'
    template_name = 'cart.html'
    title = 'Cart'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class CheckoutView(LoginRequiredMixin, TemplateView):
    login_url = '/store/login/'
    template_name = 'checkout.html'
    title = 'Checkout'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class AddToCartForm(forms.Form):
    product_id = forms.ModelChoiceField(queryset=Product.objects.all())


class AddToCartView(LoginRequiredMixin, View):
    login_url = '/store/login/'

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
                return redirect(request.META.get('HTTP_REFERER', '/'))

            cart, created = UserCart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product)

            if not created:
                in_stock = cart_item.quantity + 1 >= product.quantity
                if not in_stock:
                    self._err_out_of_stock(request, product)
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                cart_item.quantity += 1

            cart_item.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class RemoveFromCartForm(forms.Form):
    product_id = forms.ModelChoiceField(queryset=Product.objects.all())
    remove_all = forms.BooleanField(required=False)


class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = '/store/login/'

    def post(self, request, *args, **kwargs):
        form = RemoveFromCartForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product_id']
            remove_all = form.cleaned_data['remove_all']

            try:
                cart = UserCart.objects.get(user=request.user)
                cart_item = CartItem.objects.get(cart=cart, product=product)

                if remove_all:
                    cart_item.delete()
                    messages.success(
                        request, f"{product.name} removed from cart.")
                else:
                    if cart_item.quantity > 1:
                        cart_item.quantity -= 1
                        cart_item.save()
                        messages.success(
                            request, f"Removed one {product.name} from cart.")
                    else:
                        cart_item.delete()
                        messages.success(
                            request, f"Last {product.name} removed from cart.")

            except (UserCart.DoesNotExist, CartItem.DoesNotExist):
                messages.error(request, "Item not found in cart.")

            finally:
                return redirect(request.META.get('HTTP_REFERER', '/'))

        messages.error(request, "Invalid request.")
