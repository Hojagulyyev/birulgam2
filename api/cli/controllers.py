from . import product


controllers = {
    "get_products": product.controllers.get_products_controller,
    "create_product": product.controllers.create_product_controller,
}
