from modeltranslation.translator import translator, TranslationOptions
from .models import UserCart, CartItem

class UserCartTranslationOptions(TranslationOptions):
    fields = ('user',)

class CartItemTranslationOptions(TranslationOptions):
    fields = ('product',)


translator.register(UserCart, UserCartTranslationOptions)
translator.register(CartItem, CartItemTranslationOptions)
