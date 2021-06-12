from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm

from .models import Color, Category, Cart, CartProduct, Customer, Product


class TrouserAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='trousers'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ShortsAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='shorts'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)