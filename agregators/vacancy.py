class Vacancy:
    '''Vacancy class implementation'''
    def __init__(self, language, payment_from=None,
                 payment_to=None, currency='RUR'):
        self.__programming_language = language
        self.__payment_from = payment_from
        self.__payment_to = payment_to
        self.__currency = currency

    def get_programming_language(self):
        '''Programming language getter'''
        return self.__programming_language

    def get_payment_from(self):
        '''Payment_from getter'''
        return self.__payment_from

    def get_payment_to(self):
        '''Payment_to getter'''
        return self.__payment_to

    def get_currency(self):
        '''Currency getter'''
        return self.__currency

    def predict_rub_salary(self):
        '''Calculate average salary'''
        if ((not self.__payment_from) and (not self.__payment_to)) or \
            ((self.__currency != 'RUR') and (self.__currency != 'rub')):
            return None
        elif (self.__payment_from) and (not self.__payment_to):
            return int(self.__payment_from * 1.2)
        elif (self.__payment_to) and (not self.__payment_from):
            return int(self.__payment_to * 0.8)
        return int((self.__payment_from + self.__payment_to) // 2)
