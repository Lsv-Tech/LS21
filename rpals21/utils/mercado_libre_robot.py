from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from robotsearch import RobotSearch
from settings_webdriver import driver, get_element


class MercadoLibreBot(RobotSearch):
    url: str = 'https://www.mercadolibre.com.co/'

    def __init__(self, drivers):
        super().__init__()
        self.driver = drivers

    def login(self, user, password):
        self.driver.find_element_by_class_name('option-login').click()
        self.driver.find_element_by_name('user_id').send_keys(user, Keys.ENTER)
        get_element(By.NAME, 'password').send_keys(password, Keys.ENTER)

    def find_products(self):
        self.driver.find_element_by_name('as_word').send_keys(
            self.search or 'celulares', Keys.ENTER)

        for index in range(0, self.paginate_by):
            catalogue = self.driver.find_elements(By.CLASS_NAME, 'results-item')
            self.iterate_catalogue(catalogue)
            try:
                self.next_page()
            except:
                break

    def next_page(self):
        "When you finish iterating over the current page, go to the next"
        driver.find_element_by_class_name('prefetch').click()

    def iterate_catalogue(self, catalogue):
        for product in catalogue:
            name = self.exist_element(product, by=By.CLASS_NAME, value='main-title')
            price = f"${self.exist_element(product, by=By.CLASS_NAME, value='price__fraction')}"
            origin = self.exist_element(product, by=By.CLASS_NAME, value='item__condition')
            shipping = self.exist_element(product, by=By.CLASS_NAME, value='stack-item-info')

            print(name, price)

    @property
    def total_products(self):
        return self.driver.find_element_by_class_name('quantity-results').text


m = MercadoLibreBot(driver)
m.search = 'zapatos'
m.run()
