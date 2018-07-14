import os
import time
from selenium.webdriver.chrome.webdriver import WebDriver

BASE_DIR = os.path.dirname(__file__)
driver = WebDriver(executable_path=os.path.join(BASE_DIR, 'Driver', 'chromedriver'))


class Articulo:
    def __init__(self, titulo, precio, link):
        self.titulo = titulo
        self.precio = int(precio.replace('.', ''))
        self.link = link

    def __str__(self):
        return self.precio


class Scrap:

    l_articulos = []
    driver.get('https://www.mercadolibre.com.co/')

    def page(self):
        try:
            li = driver.find_element_by_class_name("pagination__next")
            next_link = li.find_element_by_tag_name('a').get_attribute('href')
            while next_link != "#":
                time.sleep(1)
                self.run()
                driver.find_element_by_class_name('pagination__next').click()

                li = driver.find_element_by_class_name("pagination__next")
                next_link = li.find_element_by_tag_name('a').get_attribute('href')
                print(next_link)
                if "#" in next_link:
                    break

        except:
            self.run()

    def run(self):
        info = driver.find_element_by_id('searchResults')
        ac = info.find_elements_by_tag_name('li')
        for a in ac:
            self.l_articulos.append(Articulo(a.find_element_by_class_name('main-title').text,
                                             a.find_element_by_class_name('price__fraction').text,
                                             a.find_element_by_tag_name('a').get_attribute('href')))

    def generar_articulos(self, string, min, max):

        try:
            search = driver.find_element_by_name('as_word')
            search.send_keys(string)
            button = driver.find_element_by_class_name('nav-icon-search')
            button.click()
            minimo = driver.find_element_by_id('fromPrice')
            minimo.send_keys(min)
            time.sleep(2)
            maximo = driver.find_element_by_id('toPrice')
            maximo.send_keys(max)
            button_r = driver.find_element_by_xpath('//*[@id="priceForm"]/div/button')
            button_r.click()
            time.sleep(2)
            results=driver.find_element_by_class_name('quantity-results')
            print(results.text)
            self.page()
        finally:
            time.sleep(10)
            driver.close()
            driver.quit()


art = Scrap()
art.generar_articulos('calculadora', '5000', '10000')
