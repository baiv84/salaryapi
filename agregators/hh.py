import requests
from .vacancy import Vacancy


class HeadHunterJobAgregator:
    '''HH.RU vacancies grabber engine'''
    def __init__(self, language, area=1, period=30,
                 exclude_words=['менеджер', 'консультант', 'продавец',
                                'поддержки', 'поддержка', 'пользователей', ]):
        self.__vacancies_list = []
        self.__language = language
        self.__area = area
        self.__period = period
        self.__exclude_words = ' not '.join(exclude_words)
        self.build_vacancies_list()

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

    def vacancies_paginator(self, page):
        '''Return particular page vacancies'''
        vacancies_list = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }
        params = {
              'text': f'{self.__language} not {self.__exclude_words} !(разработчик or программист or инженер or developer or programmer or engineer)',
              'only_with_salary': True,
              'area': self.__area,
              'period': self.__period,
              'page': page,
              'per_page': 100,
              'search_field': 'name',
        }
        response = requests.get('https://api.hh.ru/vacancies/',
                                params=params, headers=headers)
        response.raise_for_status()
        raw_vacancies = response.json()['items']

        for raw_vacancy in raw_vacancies:
            salary = raw_vacancy['salary']
            payment_from = salary['from']
            payment_to = salary['to']
            currency = salary['currency']
            vacancy = Vacancy(self.__language, payment_from, payment_to, currency)
            vacancies_list.append(vacancy)
        return vacancies_list

    def calculate_average_salary(self):
        '''Calculate average salary for programming language'''
        average_salary = None
        handled_vacancies = [vac.predict_rub_salary() for vac in self.__vacancies_list if vac.predict_rub_salary()]
        handled_vacancies_count = len(handled_vacancies)

        if handled_vacancies_count > 0:
            average_salary = sum(handled_vacancies) // handled_vacancies_count
        return (self.get_vacancies_number(),
                handled_vacancies_count, average_salary,)

    def get_vacancies_number(self):
        '''Return vanacies number of particular programming language'''
        return len(self.__vacancies_list)

    def get_programming_language(self):
        '''Return programming language name'''
        return self.__language