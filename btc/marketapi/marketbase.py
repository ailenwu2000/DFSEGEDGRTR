from abc import ABCMeta, abstractmethod, abstractproperty


class Balance(dict):
    __metaclass__ = ABCMeta

    @abstractproperty
    def cny(self) -> float:
        pass

    @abstractproperty
    def usd(self) -> float:
        pass

    @abstractproperty
    def btc(self) -> float:
        pass

    @abstractmethod
    def coin_balance(self, coin) -> float:
        pass


class Deep(dict):
    __metaclass__ = ABCMeta

    @abstractproperty
    def bid_price(self) -> float:
        pass

    @abstractproperty
    def bid_amount(self) -> float:
        pass

    @abstractproperty
    def ask_price(self) -> float:
        pass

    @abstractproperty
    def ask_amount(self):
        pass

    @property
    def mid_price(self):
        return (self.askprice+self.bidprice)/2

    @property
    def mid_percent(self):
        return (self.askprice-self.bidprice)/self.midprice


class MarketBase(object):
    __metaclass__ = ABCMeta

    def balance(self) -> Balance:
        pass

    def deep(self) -> Deep:
        pass
