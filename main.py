from web_scraper import WebScraper

if __name__ == '__main__':
    scraper = WebScraper('https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/cala-polska?page=', 'zł/m²')

    scraper.print_average(1)
