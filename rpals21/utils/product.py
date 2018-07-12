
class Product:

    def __init__(self, name, original_price, discount,
                 price_secondary, detail, image, shipping):
        self.name = name
        self.original_price = original_price
        self.discount = discount
        self.price_secondary = price_secondary
        self.detail = detail
        self.image = image

    def __str__(self):
        return self.name