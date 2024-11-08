from modeltranslation.translator import translator, TranslationOptions
from .models import MyUser


class MyUserTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name')


translator.register(MyUser, MyUserTranslationOptions)
