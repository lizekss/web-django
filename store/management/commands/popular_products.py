from django.core.management.base import BaseCommand
from django.db.models import Count
from store.models import Product

class Command(BaseCommand):
    help = 'Find the top 3 most popular products in users’ carts'

    def handle(self, *args, **kwargs):
        result = (
            Product.objects
            .annotate(user_count=Count('cartitem__cart__user', distinct=True))
            .order_by('-user_count')[:3]
        )

        if result:
            self.stdout.write("Top 3 most popular products:")
            for i, product in enumerate(result):
                self.stdout.write(f"{i + 1}. {product.name} - in {product.user_count} users' carts")
        else:
            self.stdout.write("No products found.")
