import os
import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

BASE_DIR = os.path.dirname(__file__)


class Articulo:
    def __init__(self, titulo, precio, link):
        self.titulo = titulo
        self.precio = int(precio.replace('.', ''))
        self.link = link

    def __str__(self):
        return self.precio


class Scrap:

    def __init__(self):

        # creating configurations to the driver
        options = Options()
        options.add_argument('start-maximized')
        options.add_argument('--incognito')

        self.l_articulos = []
        self.driver = WebDriver(
            executable_path=os.path.join(BASE_DIR, 'Driver', 'chromedriver'),
            options=options
        )
        self.driver.get('https://www.mercadolibre.com.co/')

    def page(self):
        try:
            li = self.driver.find_element_by_class_name("pagination__next")
            next_link = li.find_element_by_tag_name('a').get_attribute('href')
            while next_link != "#":
                time.sleep(1)
                self.run()
                self.driver.find_element_by_class_name('pagination__next').click()

                li = self.driver.find_element_by_class_name("pagination__next")
                next_link = li.find_element_by_tag_name('a').get_attribute('href')
                if "#" in next_link:
                    break

        except:
            self.run()

    def run(self):
        info = self.driver.find_element_by_id('searchResults')
        ac = info.find_elements_by_tag_name('li')
        for a in ac:
            self.l_articulos.append(Articulo(a.find_element_by_class_name('main-title').text,
                                             a.find_element_by_class_name('price__fraction').text,
                                             a.find_element_by_tag_name('a').get_attribute('href')).__dict__)

    def generar_articulos(self, string, min='0', max='0'):

        try:
            search = self.driver.find_element_by_name('as_word')
            search.send_keys(string)
            button = self.driver.find_element_by_class_name('nav-icon-search')
            button.click()
            # minimo = self.driver.find_element_by_id('fromPrice')
            # minimo.send_keys(min)
            # time.sleep(5)
            # maximo = self.driver.find_element_by_id('toPrice')
            # maximo.send_keys(max)
            button_r = self.driver.find_element_by_xpath('//*[@id="priceForm"]/div/button')
            button_r.click()
            time.sleep(5)
            self.page()
            # return self.l_articulos
        finally:
            time.sleep(10)
            self.driver.close()
            self.driver.quit()
