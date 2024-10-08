from django.contrib import admin

from store.models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'category_tree')
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
