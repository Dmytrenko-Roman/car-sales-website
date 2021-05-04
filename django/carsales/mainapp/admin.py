from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

from PIL import Image

class CarAdminForm(ModelForm):



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            f"""<span style="color:red;">If you upload images with bigger than max 
            {Product.MAX_RESOLUTION} resolution it will be cut</span>"""
        )

    #def clean_image(self):
        #image = self.cleaned_data['image']
        #img = Image.open(image)
        #min_height, min_width = Product.MIN_RESOLUTION
        #max_height, max_width = Product.MAX_RESOLUTION
        #if image.size > Product.MAX_IMAGE_SIZE:
            #raise ValidationError('Uploaded image has wrong size (>3MB)')
        #if img.height < min_height or img.width < min_width:
            #raise ValidationError('Uploaded image has too small resolution')
        #if img.height > max_height or img.width > max_width:
            #raise ValidationError('Uploaded image has too big resolution')
       #return image


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

