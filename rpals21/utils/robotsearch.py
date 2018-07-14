class RobotSearch:
    def __init__(self):
        self._search = None
        self.paginate_by = 5

    @property
    def search(self):
        return self._search or ''

    @search.setter
    def search(self, value):
        self._search = value

    def login(self, user, password):
        pass

    def find_products(self):
        pass

    def next_page(self, *args, **kwargs):
        pass

    def exist_element(self, product, **kwargs):
        try:
            return product.find_element(**kwargs).text
        except:
            return None

    def close(self):
        self.driver.close()
        self.driver.quit()

    def run(self):
        self.driver.get(self.url)
        self.find_products()
        self.close()
