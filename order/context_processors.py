from order.models import UserCart, CartItem


def cart_item_count(request):
    if request.user.is_authenticated:
        try:
            cart = UserCart.objects.get(user=request.user)
            cart_count = CartItem.objects.filter(cart=cart).count()
        except UserCart.DoesNotExist:
            cart_count = 0
    else:
        cart_count = 0

    return {'cart_count': cart_count}
