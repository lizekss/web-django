from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.placeholder import OnStoragePlaceholderImage


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    categories = models.ManyToManyField(Category, related_name='products')
    image = VersatileImageField(upload_to='products/', blank=True, null=True, placeholder_image=OnStoragePlaceholderImage(
        path='products/default.jpg'
    ))

    def __str__(self):
        return self.name
