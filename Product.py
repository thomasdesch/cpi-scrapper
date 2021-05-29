class Product():

    def __init__(self):
        self._name = None
        self._weight = None
        self._brand = None
        self._price = None
        self._category = None
        self._price_per_1000 = None
        pass
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        del self._name

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = float(value)

    @price.deleter
    def price(self):
        del self._price

    @property
    def weight(self):

        return self._weight

    @weight.setter
    def weight(self, value):

        self._weight = float(value)

    @weight.deleter
    def weight(self):

        del self._weight

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):

        self._brand = value

    @brand.deleter
    def brand(self):

        del self._brand

    @property
    def category(self):
        return self._category

    @name.setter
    def category(self, value):
        self._category = value

    @name.deleter
    def category(self):
        del self._category


    @property
    def price_per_1000(self):

        return self._price_per_1000

    @name.setter
    def price_per_1000(self, value):
        self._price_per_1000 = value

    @name.deleter
    def price_per_1000(self):
        del self._price_per_1000
