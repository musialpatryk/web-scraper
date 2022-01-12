from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class WebScraper:
    def __init__(self, url, print_suffix):
        self.__url = url
        self.__print_suffix = print_suffix
        self.__browser = self.__get_webdriver()
        self.__all_prices = []

    def print_average(self, page_count):
        self.__all_prices = []
        self.__get_prices_from_pages(page_count)
        print('Average cost per meter is:', "%.2f" % self.__compute_average(self.__all_prices), self.__print_suffix)

    def __get_webdriver(self):
        options = Options()
        options.headless = True
        options.add_argument("--log-level=3")

        s = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=s, options=options)

    def __get_all_descriptions(self, url):
        self.__browser.get(url)
        apartments = self.__browser.find_elements(By.TAG_NAME, 'article')

        descriptions = []
        for apartment in apartments:
            paragraphs = apartment.find_elements(By.TAG_NAME, 'p')
            for paragraph in paragraphs:
                descriptions.append(paragraph)

        return descriptions

    def __remove_suffix_from_price(self, price_text):
        removed_whitespaces = "".join(price_text.split())
        clear_price = removed_whitespaces.replace(self.__print_suffix, '')
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
            apartments_descriptions = self.__get_all_descriptions(self.__url + str(i))
            self.__all_prices.extend(self.__get_prices(apartments_descriptions))