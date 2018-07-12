from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from robotsearch import RobotSearch
from settings_webdriver import driver, get_element


class LinioBot(RobotSearch):
    url: str = 'https://www.linio.com.co/'

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def login(self, user, password):
        self.driver.find_element_by_xpath("//*[@id='navbar']/div[1]/div[3]/a[2]/span").click()
        get_element(By.XPATH, value="//*[@id='user-menu']/ul/li[1]/a").click()
        self.driver.find_element_by_id('login_form_email').send_keys(user)
        self.driver.find_element_by_id('login_form_password').send_keys(password, Keys.ENTER)

    def find_products(self):
        get_element(By.NAME, value='q') \
            .send_keys(self.search or 'celulares', Keys.ENTER)

        for cont in range(2, self.paginate_by + 1):
            catalogue = driver.find_elements_by_class_name('catalogue-product')
            self.iterate_catalogue(catalogue)
            page = self.next_page(cont)
            self.driver.get(page)

    def iterate_catalogue(self, catalogue):
        for product in catalogue:
            get_element(By.CSS_SELECTOR, '.image-container img')
            name = product.find_element_by_css_selector(".image-container img").get_property('alt')
            url_image = product.find_element_by_css_selector(".image-container img").get_property('src')
            original_price = self.exist_element(product, by=By.CLASS_NAME, value='original-price')
            discount = self.exist_element(product, by=By.CLASS_NAME, value='discount')
            price_secondary = self.exist_element(product, by=By.CLASS_NAME, value="price-secondary")

            """
            Solo hace falta anexar el objecto que almacena en los productos
            hay una clase en el archivo product.py que tiene el objecto producto
            """
            print(name)

    def next_page(self, number_page):
        paginator = self.get_paginator()
        page = f"{paginator[0].get_property('href')}?page={number_page}"
        return page

    @property
    def total_products(self):
        return driver.find_element_by_class_name('highlight').text

    @property
    def total_pages(self):
        paginators = self.get_paginator()
        last_href = paginators[-1].get_property('href')
        total_pages = int(last_href.split(sep='=')[-1])
        return total_pages

    def get_paginator(self):
        return driver.find_elements_by_css_selector(".pagination-container .page-link")


linio = LinioBot(driver)
linio.search = 'zapatos'
linio.run()
