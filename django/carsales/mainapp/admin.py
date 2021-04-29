from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin
from django.forms import ModelChoiceField

from .models import *


class CarAdminForm(ModelForm):

    MIN_RESOLUTION = (400, 400)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = f'Upload images with minimal resolution {self.MIN_RESOLUTION}'


class CarAdmin(admin.ModelAdmin):

    form = CarAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='cars'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class DetailAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='details'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Car, CarAdmin)
admin.site.register(Detail, DetailAdmin)
admin.site.register(FavoriteProduct)
admin.site.register(Favorites)
admin.site.register(Customer)

