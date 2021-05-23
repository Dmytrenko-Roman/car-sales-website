from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, View

from .models import Car, Detail, Category, LatestProducts, Customer, Favorites, FavoriteProduct
from .mixins import CategoryDetailMixin


class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_bar()
        products = LatestProducts.objects.get_products_for_main_page('car', 'detail')
        context = {
            'categories': categories,
            'products': products
        }
        return render(request, 'base.html', context)


class ProductDetailView(CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'car': Car,
        'detail': Detail
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context


class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'


class AddToFavoritesView(View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        customer = Customer.objects.get(user=request.user)
        favorites = Favorites.objects.get(owner=customer)
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        favorite_product = FavoriteProduct.objects.create(
            user=favorites.owner, favorites=favorites, content_object=product, final_price=product.price
        )
        favorites.products.add(favorite_product)
        return HttpResponseRedirect('/favorites/')



class FavoritesView(View):

    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        favorites = Favorites.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_bar()
        context = {
            'favorites': favorites,
            'categories': categories
        }
        return render(request, 'favorites.html', context)
