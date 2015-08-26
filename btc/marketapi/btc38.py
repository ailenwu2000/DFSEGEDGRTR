# --*-- coding: utf-8 --*--
import requests
import time
import hashlib
import json


class Balance(dict):
    @property
    def cny(self) -> float:
        return self.coin_balance('cny')

    @property
    def btc(self) -> float:
        return self.coin_balance('btc')

    def coin_balance(self, coin) -> float:
        return float(self[coin+'_balance'])


class Deep(dict):
    @property
    def bid_price(self) -> float:
        return float(self['bids'][0][0])

    @property
    def bid_amount(self) -> float:
        return float(self['bids'][0][1])

    @property
    def ask_price(self) -> float:
        return float(self['asks'][0][0])

    @property
    def ask_amount(self):
        return float(self['asks'][0][1])

    @property
    def mid_price(self):
        return (self.askprice+self.bidprice)/2

    @property
    def mid_percent(self):
        return (self.askprice-self.bidprice)/self.midprice


class OpenOrder(list):
    pass


class OrderHistory(list):
    pass


class BTC38API(object):
    url_balance = 'http://www.btc38.com/trade/t_api/getMyBalance.php'
    url_open_order = 'http://www.btc38.com/trade/t_api/getOrderList.php'
    url_cancel_order = 'http://www.btc38.com/trade/t_api/cancelOrder.php'
    url_submit_order = 'http://www.btc38.com/trade/t_api/submitOrder.php'
    url_trades = 'http://api.btc38.com/v1/trades.php?c=%s&mk_type=%s'
    url_deep = 'http://api.btc38.com/v1/depth.php?c=%s&mk_type=%s'

    def __init__(self, public_key, private_key, user_id):
        self.public_key = public_key
        self.private_key = private_key
        self.user_id = user_id

    @staticmethod
    def _get_headers():
        return {'User-Agent':
                'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

    def _post(self, url, dict_data=None):
        timestamp = str(int(time.time()))
        mdt = '%s_%s_%s_%s' % (self.public_key, self.user_id, self.private_key, timestamp)
        md5 = hashlib.md5(mdt.encode('utf-8')).hexdigest().upper()
        data = {'key': self.public_key, 'time': timestamp, 'md5': md5}
        if dict_data:
            data.update(dict_data)
        rsp = requests.post(url, data=data, headers=self._get_headers())
        if rsp.status_code == 200:
            return rsp.text
        else:
            raise Exception(rsp.status_code, rsp.text)

    def _get(self, url):
        rsp = requests.get(url, headers=self._get_headers())
        if rsp.status_code == 200:
            return rsp.text
        else:
            raise Exception(rsp.status_code, rsp.text)

    def balance(self):
        r = self._post(self.url_balance, {})
        return Balance(json.loads(r))

    def deep(self, coin, market):
        url = self._get_deep_url(coin, market)
        r = self._get(url)
        return Deep(json.loads(r))

    def open_order(self, mk_type, coin=None):
        url = self.url_open_order
        dict_data = {'mk_type': mk_type}
        if coin:
            dict_data['coinname'] = coin

        r = self._post(url, dict_data)

        if r.find('[') > -1:
            return OpenOrder(json.loads(r))
        else:
            return OpenOrder([])

    def cancel(self, mk_type, order_id):
        url = self.url_cancel_order
        r = self._post(url, {'mk_type': mk_type, 'order_id': order_id})
        if r != 'succ':
            raise Exception(r)

    def cancel_all_order(self, coin=None):
        for order in self.open_order(mk_type='cny', coin=coin):
            self.cancel('cny', order['id'])

        for order in self.open_order(mk_type='btc', coin=coin):
            self.cancel('btc', order['id'])

    def _round_price(self, mk_type, price):
        if mk_type == 'btc':
            return round(price, 8)
        else:
            return round(price, 5)

    def _round_amount(self, amount):
        return round(amount, 6)

    def sell(self, mk_type, amount, price, coinname):
        url = self.url_submit_order
        price = self._round_price(mk_type, price)
        amount = self._round_amount(amount)

        r = self._post(url,
                       {'type': 2, 'mk_type': mk_type, 'amount': amount, 'price': price, 'coinname': coinname})
        if r != 'succ':
            raise Exception(r)

    def buy(self, mk_type, amount, price, coinname):
        url = self.url_submit_order
        price = self._round_price(mk_type, price)
        amount = self._round_amount(amount)

        r = self._post(url,
                       {'type': 1, 'mk_type': mk_type, 'amount': amount, 'price': price, 'coinname': coinname})
        if r != 'succ':
            raise Exception(r)

    def orderhistory(self, mk_type, coin):
        url = self._get_trades_url(coin, mk_type)
        r = self._get(url)
        if r.find('[') > -1:
            return OrderHistory(json.loads(r))
        else:
            return OrderHistory([])

    def test(self):
        print('test balance', self.balance())
        print('test deep btc', self.deep('btc','cny'))
        print('test openorder cny', self.open_order('cny'))
        print('test openorder cny nxt', self.open_order(mk_type='cny', coin='nxt'))
        #print('sell test')
        #self.sell(mk_type='cny',amount=0.001,price=2000,coinname='btc')
        #print('buy test')
        #self.buy(mk_type='cny',amount=0.001,price=1000,coinname='btc')
        #print('test openorder cny',self.openorder('cny'))
        #print('test cancel all order')
        #self.cancelallorder()
        #print(self.orderhistory(mk_type='cny',coin='btc')[-1])

if __name__ == '__main__':
    api = BTC38API(public_key='F640152064FDA8C5DFE5D950036EC706',
                   private_key='82FC35C7D75C4E85E4086F31B22B5CEC',
                   user_id='34895')
    api.test()
