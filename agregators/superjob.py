import time
import requests
import datetime
from .vacancy import Vacancy


class SuperJobAgregator:
    '''SUPERJOB.RU vacancies grabber engine'''
    def __init__(self, superjob_api_key, language, catalogues=[48],
                 town='Moscow', exclude_words=['менеджер', 'консультант', 'продавец',
                                               'поддержки', 'поддержка', 'пользователей',]):
        self.__vacancies_list = []
        self.__superjob_api_key = superjob_api_key
        self.__language = language
        self.__catalogues = ','.join(map(lambda catalogue: str(catalogue), catalogues))
        self.__town = town
        self.__exclude_words = ','.join(exclude_words)
        self.build_vacancies_list()

    def get_vacancies_number(self):
        '''Return vanacies number of particular programming language'''
        return len(self.__vacancies_list)

    def get_programming_language(self):
        '''Return programming language name'''
        return self.__language

    def vacancies_paginator(self, page):
        '''Return particular page vacancies'''
        today = datetime.date.today()
        date_published_from = (today - datetime.timedelta(days=30))
        date_published_from = int(time.mktime(date_published_from.timetuple()))

        vacancies_list = []
        headers = {'X-Api-App-Id': self.__superjob_api_key}
        params = {
                'keywords[0][keys]': self.__language + ',программист',
                'keywords[0][skwc]': 'and',
                'keywords[0][srws]': 4,
                'keywords[1][keys]': self.__language + ',разработчик',
                'keywords[1][skwc]': 'and',
                'keywords[1][srws]': 4,
                'keywords[2][keys]': self.__language + ',developer',
                'keywords[2][skwc]': 'and',
                'keywords[2][srws]': 4,
                'keywords[3][keys]': self.__language + ',programmer',
                'keywords[3][skwc]': 'and',
                'keywords[3][srws]': 4,
                'keywords[4][keys]': self.__language + ',инженер',
                'keywords[4][skwc]': 'and',
                'keywords[4][srws]': 4,
                'keywords[5][keys]': self.__language + ',engineer',
                'keywords[5][skwc]': 'and',
                'keywords[5][srws]': 4,
                'keywords[6][keys]': self.__exclude_words,
                'keywords[6][skwc]': 'nein',
                'catalogues': self.__catalogues,
                'date_published_from': date_published_from,
                'town': self.__town,
                'count': 100,
                'page': page
        }
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                params=params, headers=headers)
        response.raise_for_status()
        raw_vacancies = response.json()['objects']
        for raw_vacancy in raw_vacancies:
            payment_from = raw_vacancy['payment_from']
            payment_to = raw_vacancy['payment_to']
            currency = raw_vacancy['currency']
            vacancy = Vacancy(self.__language, payment_from, payment_to, currency)
            vacancies_list.append(vacancy)
        return vacancies_list

    def build_vacancies_list(self):
        '''Build vacancies list of particular programming language'''
        page = 0
        self.__vacancies_list = []
        while True:
            vacancies_per_page = self.vacancies_paginator(page)
            self.__vacancies_list = (self.__vacancies_list + vacancies_per_page)
            if len(vacancies_per_page) < 100:
                break
            page += 1

    def calculate_average_salary(self):
        '''Calculate average salary for programming language'''
        average_salary = None
        handled_vacancies = [vac.predict_rub_salary() for vac in self.__vacancies_list if vac.predict_rub_salary()]
        handled_vacancies_count = len(handled_vacancies)

        if handled_vacancies_count > 0:
            average_salary = sum(handled_vacancies) // handled_vacancies_count
        return (self.get_vacancies_number(),
                handled_vacancies_count, average_salary, )
