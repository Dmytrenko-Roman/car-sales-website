from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse


User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__.meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        respect_to = kwargs.get('respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if respect_to:
            ct_model = ContentType.objects.filter(model=respect_to)
            if ct_model.exists():
                if respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(respect_to), reverse=True)
        return products


class LatestProducts:

    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    CATEGORY_COUNT_NAME = {
        'Cars': 'car__count',
        'Details': 'detail__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_bar(self):
        models = get_models_for_count('car', 'detail')
        qs = list(self.get_queryset().annotate(*models).values())
        return [dict(name=c['name'], slug=c['slug'], count=c[self.CATEGORY_COUNT_NAME[c['name']]]) for c in qs]


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Category name')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Product name')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Image')
    description = models.TextField(verbose_name='Description', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.title


class Car(Product):


    model = models.CharField(max_length=255, verbose_name='Model')
    brand = models.CharField(max_length=255, verbose_name='Brand (Car)')
    year = models.CharField(max_length=255, verbose_name='Year')
    engine_volume = models.CharField(max_length=255, verbose_name='Engine Volume')
    country_of_purchase = models.CharField(max_length=255, verbose_name='Country Of Purchase')
    number_of_owners = models.PositiveIntegerField(default=1, verbose_name='Number Of Owners')
    is_american = models.BooleanField(default=False, verbose_name='Is American')

    def __str__(self):
        return f'{self.category.name}: {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Detail(Product):

    brand = models.CharField(max_length=255, verbose_name='Brand (Detail)')
    suitable_models = models.CharField(max_length=255, verbose_name='Suitable Models')
    wear = models.CharField(max_length=255, verbose_name='Wear')

    def __str__(self):
        return f'{self.category.name}: {self.title}'

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class FavoriteProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Buyer', on_delete=models.CASCADE)
    favorites = models.ForeignKey('Favorites', verbose_name='Favorites', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='FinalPrice')

    def __str__(self):
        return f"Product: {self.content_object.title} (for favorites)"


class Favorites(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Owner', on_delete=models.CASCADE)
    products = models.ManyToManyField(FavoriteProduct, blank=True, related_name="related_favorites")
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='FinalPrice')
    in_order = models.BooleanField(default=True)
    for_anonymous_users = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, verbose_name='Phone Number')
    address = models.CharField(max_length=255, verbose_name='Address')

    def __str__(self):
        return f'User {self.user.first_name} {self.user.last_name}'

