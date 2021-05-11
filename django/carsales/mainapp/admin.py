from django.forms import ModelChoiceField
from django.contrib import admin

from .models import *

from PIL import Image


# class CarAdminForm(ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         instance = kwargs.get('instance')
#         if not instance.sd:
#             self.fields['sd_volume_max'].vidget.attrs.update({
#                 'readonly': True, 'style': 'background: lightgray'
#             })
#
#     def clean(self):
#         if not self.cleaned_data['sd']:
#             self.cleaned_data['sd_volume_max'] = None
#         return self.cleaned_data


class CarAdmin(admin.ModelAdmin):

    # change_form_template = 'admin.html'
    # form = CarAdminForm

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

