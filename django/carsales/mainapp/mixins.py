from django.views.generic.detail import SingleObjectMixin

from .models import Category

class CategoryDetailMixin(SingleObjectMixin):
    pass
