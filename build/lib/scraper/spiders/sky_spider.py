from datetime import date
from scrapy.spider import BaseSpider
from scraper.items import Flight
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import re
import time

ITEMS_TO_SKIP = ['no_flights_oneway', 'no_flights_return']


class SkySpider(BaseSpider):
    name = "sky"
    allowed_domains = ["skyscanner.net"]
    default = "http://www.skyscanner.net/flights/bts/"
    start_urls = ["http://www.skyscanner.net/flights/"]
    monthly = True

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
                    dat = kwargs['date']
                    if re.match('\d{6}', dat):
                        self.monthly = False
                        self.start_urls[0] += '/' + dat
                    elif re.match('\d{4}', dat):
                        self.monthly = True
                        self.start_urls[0] += ('/blah.html?oym=' + dat +
                                               '&charttype=1')
                    else:
                        self.this_month()
                else:
                    self.this_month()
                if self.monthly and 'rtn' in kwargs:
                    self.rtn = kwargs['rtn']
                    self.start_urls[0] += '&rtn=' + self.rtn
                else:
                    self.rtn = '0'
                url = self.start_urls[0]

        self.driver.get(url)

    def this_month(self):
        this_month = date.today().isoformat().split('-')[1]
        self.start_urls[0] += ('/blah.html?oym=' + this_month + '&charttype=1')
        self.monthly = True

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
        time.sleep(2.5)

        items = []

        if self.monthly:
            outbound = self.driver.find_element_by_id('outboundChart')

            items = self.get_items(outbound)

            if self.rtn == '1':
                inbound = self.driver.find_element_by_id('inboundChart')
                items += self.get_items(inbound)
        else:
            day_list = self.driver.find_element_by_id('day_oneway')
            for row in day_list.find_elements_by_class_name('row'):
                # item['date'] =
                item = Flight()
                carr = row.find_elements_by_class_name('carr')[0]
                if carr.tag_name == 'p':
                    item['company'] = carr.text
                else:
                    item['company'] = carr.get_attribute('alt')
                item['price'] = row.find_elements_by_class_name('px')[0].text
                item['orig'] = row.find_elements_by_class_name('sta-dep')[0].text
                item['dest'] = row.find_elements_by_class_name('sta-arr')[0].text
                items.append(item)

        return items
