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
        parsed_html = BeautifulSoup(self.index.text, convertEntities=BeautifulSoup.HTML_ENTITIES)
        self.restaurant_name = "Mjam"
        bodyNode = parsed_html.body
        if bodyNode is not None:
            nameNode = bodyNode.find('h1', attrs={'property': 'name'})
            if nameNode is not None:
                self.restaurant_name = nameNode.text
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
        if m is not None:
            self.order_eta = m.group(1)
            return self.order_eta
        else:
            return 'not loaded yet'

    def loadOrderItems(self):
        items_url = "https://www.mjam.net/ajax/restaurant/graz/mampf/cart/getDeltas/"
        items_resp = self.session.post(url=items_url)
        items = json.loads(items_resp.text)

        meta          = items['meta']
        waiting_for = meta['waiting_for']

        tmp_orderer = dict()
        orders = dict()
        for changeset in items['changesets']:
            message = changeset['message']
            action     = message['action']
            sid          = message['session_key']
            data       = message['data']

            if action == 'cartRename':
                if sid in tmp_orderer:
                    print "ERROR???"
                else:
                    tmp_orderer[sid] = data['name']
            elif action == 'itemQuantity':
                item = data['item']
                if sid in orders:
                    orders[sid].append(item['name'])
                else:
                    orders[sid] = [item['name']]

        for orderer in tmp_orderer:
            orderer_name = tmp_orderer[orderer]
            orders[orderer_name] = orders.pop(orderer)

        return orders, waiting_for

