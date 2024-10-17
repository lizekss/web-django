from django.contrib import admin

from store.models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity',
                    'total_stock_value', 'get_categories')
    list_filter = ('categories', 'price')
    search_fields = ('name', 'description')
    ordering = ('name',)

    def total_stock_value(self, obj):
        return obj.price * obj.quantity
    total_stock_value.short_description = 'Total Stock Value'

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)
    ordering = ('name',)
