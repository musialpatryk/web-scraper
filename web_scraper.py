from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class WebScraper:
    def __init__(self, url, print_suffix):
        self.url = url
        self.print_suffix = print_suffix
        self.browser = self.__get_webdriver()
        self.all_prices = []

    def print_average(self, page_count):
        self.all_prices = []
        self.__get_prices_from_pages(page_count)
        print('Average cost per meter is:', "%.2f" % self.__compute_average(self.all_prices), self.print_suffix)

    def __get_webdriver(self):
        options = Options()
        options.headless = True

        s = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=s, options=options)

    def __get_all_descriptions(self, url):
        self.browser.get(url)
        apartments = self.browser.find_elements(By.TAG_NAME, 'article')

        descriptions = []
        for apartment in apartments:
            paragraphs = apartment.find_elements(By.TAG_NAME, 'p')
            for paragraph in paragraphs:
                descriptions.append(paragraph)

        return descriptions

    def __remove_suffix_from_price(self, price_text):
        removed_whitespaces = "".join(price_text.split())
        clear_price = removed_whitespaces.replace(self.print_suffix, '')
        if len(clear_price) == 0:
            return None
        return float(clear_price)

    def __get_prices(self, descriptions):
        prices = []
        for description in descriptions:
            spans = description.find_elements(By.TAG_NAME, 'span')
            if len(spans) != 3:
                continue

            price = self.__remove_suffix_from_price(spans[2].text)
            if price is not None:
                prices.append(price)
        return prices

    def __compute_average(self, prices):
        return sum(prices) / len(prices)

    def __get_prices_from_pages(self, count):
        for i in range(1, count + 1):
            print('Crawling pagination page: ' + str(i))
            apartments_descriptions = self.__get_all_descriptions(self.url + str(i))
            self.all_prices.extend(self.__get_prices(apartments_descriptions))