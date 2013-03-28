from datetime import date
from scrapy.spider import BaseSpider
from scraper.items import Flight
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time

ITEMS_TO_SKIP = ['no_flights_oneway', 'no_flights_return']


class SkySpider(BaseSpider):
    name = "sky"
    allowed_domains = ["skyscanner.net"]
    default = "http://www.skyscanner.net/flights/bts/"
    start_urls = ["http://www.skyscanner.net/flights/"]

    def __init__(self, **kwargs):
        BaseSpider.__init__(self)
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX)
        url = self.default
        if 'from' in kwargs:
            self.start_urls[0] += kwargs['from']
            if 'to' in kwargs:
                self.start_urls[0] += '/' + kwargs['to']
                if 'date' in kwargs:
                    self.start_urls[0] += ('/blah.html?oym=' + kwargs['date'] +
                                           '&charttype=1')
                else:
                    today = date.today().isoformat().split('-')
                    self.start_urls[0] += ('/blah.html?oym=' + today[0][-2:] +
                                           today[1] + '&charttype=1')
                if 'rtn' in kwargs:
                    self.rtn = kwargs['rtn']
                    self.start_urls[0] += '&rtn=' + self.rtn
                else:
                    self.rtn = '0'
                url = self.start_urls[0]

        self.driver.get(url)

    def __del__(self):
        self.driver.close()

    def get_items(self, chart):
        items = []
        for elem in chart.find_elements_by_class_name('item'):
            item = Flight()
            tooltip1 = elem.get_attribute('tooltip1')
            if tooltip1 in ITEMS_TO_SKIP:
                continue
            pricelist = elem.get_attribute('tooltip3').rsplit(' ', 1)
            atts = ['company', 'price']
            for a, l in zip(atts, pricelist):
                item[a] = l
            item['date'] = tooltip1
            from_to = elem.get_attribute('tooltip2').split(' ', 1)[0]
            from_to = from_to.split('-', 1)
            item['orig'] = from_to[0]
            item['dest'] = from_to[1]
            items.append(item)
        return items

    def parse(self, response):
        #Wait for javscript to load in Selenium
        time.sleep(2)

        outbound = self.driver.find_element_by_id('outboundChart')

        items = self.get_items(outbound)

        if self.rtn == '1':
            inbound = self.driver.find_element_by_id('inboundChart')
            items += self.get_items(inbound)

        return items
