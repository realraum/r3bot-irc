import requests
import json
import re
from BeautifulSoup import BeautifulSoup


class Mjam():

    def __init__(self, url=None, cookies=None, verify=None):
        self.session = requests.Session()
	self.session.verify = verify
        self.url = url
        if cookies is not None:
            self.session.cookies = requests.utils.cookiejar_from_dict(cookies)

    def loadOrder(self):
        self.index = self.session.get(url=self.url)
        return self.index

    def isOrderSubmitted(self):
        m = re.search('.*deine Bestellung, (.*)!.*', self.index.text)
        return m is not None

    def isOrderGone(self):
        return self.index.status_code == 403

    def getRestaurantName(self):
        parsed_html = BeautifulSoup(self.index.text)
        node = parsed_html.body.find('h1', attrs={'property': 'name'})
        if node is None:
            print "cannot find restaurant name ..."
            return "Mjam"
        else:
            self.restaurant_name = node.text
            return self.restaurant_name

    def getOrderNumer(self):
        parsed_html = BeautifulSoup(self.index.text)
        self.order_number = parsed_html.body.find(
            'input', attrs={'name': 'order_number'}).get('value')
        return self.order_number

    def getOrderer(self):
        m = re.search('.*deine Bestellung, (.*)!.*', self.index.text)
        return m.group(1)

    def loadOrderETA(self):
        orderstatus_url = "https://www.mjam.net/ajax/customer/order/info/" + \
            self.order_number
        orderstatus_resp = self.session.post(url=orderstatus_url)
        orderstatus = json.loads(orderstatus_resp.text)
        m = re.search(
            '.*sollte um (.*) ankommen.$', orderstatus['short_description'])
        self.order_eta = m.group(1)
        return self.order_eta
