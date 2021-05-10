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

@register.filter
def product_spec(product):
    print(product)
    pass