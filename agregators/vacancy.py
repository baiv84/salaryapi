class Vacancy:
    '''Vacancy class implementation'''

    currency_rates = {'USD': 75, 'EUR': 80, }

    def __init__(self, language, payment_from=None, payment_to=None,
                 link=None, currency='RUR'):
        self.__programming_language = language
        self.__payment_from = payment_from
        self.__payment_to = payment_to
        self.__link = link
        self.__currency = currency

    def get_currency_rate(self):
        '''Return currency rate to convert salaries into Rubles'''
        if self.__currency not in Vacancy.currency_rates:
            return 1
        return Vacancy.currency_rates[self.__currency]

    def predict_rub_salary(self):
        '''Calculate average salary'''
        currency_rate = self.get_currency_rate()
        if (not self.__payment_from) and (not self.__payment_to):
            return None
        elif (self.__payment_from) and (not self.__payment_to):
            return (self.__payment_from * currency_rate)
        elif (self.__payment_to) and (not self.__payment_from):
            return (self.__payment_to * currency_rate)
        return ((self.__payment_from + self.__payment_to) // 2) * currency_rate

    def get_programming_language(self):
        '''Programming language getter'''
        return self.__programming_language

    def get_payment_from(self):
        '''Payment_from getter'''
        return self.__payment_from

    def get_payment_to(self):
        '''Payment_to getter'''
        return self.__payment_to

    def get_link(self):
        '''Page link getter'''
        return self.__link

    def get_currency(self):
        '''Currency getter'''
        return self.__currency
