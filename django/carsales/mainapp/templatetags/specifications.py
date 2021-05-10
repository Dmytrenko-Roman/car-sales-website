from django import template

register = template.Library()


TABLE_HEAD = """
                <table class="table">
                  <tbody>
             """

TABLE_TAIL = """
                  </tbody>
                </table>
             """

TABLE_CONTENT = """
                    <tr>
                      <td>{name}</td>
                      <td>{value}</td>
                    </tr>
                """

PRODUCT_SPEC = {
    'car': {
        'Model': 'model',
        'Brand': 'brand',
        'Year': 'year',
        'Engine Volume': 'engine_volume',
        'Country of purchase': 'country_of_purchase',
        'Number of owners': 'number_of_owners',
        'Is American': 'is_american',
    },
    'detail': {
        'Brand': 'brand',
        'Suitable models': 'suitable_models',
        'Wear': 'wear'
    }
}

def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))


@register.filter
def product_spec(product):
    model.name = product.__class__._meta.model_name
    pass