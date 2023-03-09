import time
import datetime
import requests
from environs import Env
from common import calculate_language_statistics
from common import print_language_statistics


def get_hh_page_salaries(language, area=1, period=30, page=0, per_page=100,
                         exclude_words=['менеджер', 'консультант', 'продавец',
                                        'поддержки', 'поддержка', 'пользователей',]):
    '''HH.RU - get language salaries from search page with number=<page>'''
    exclude_words = ' not '.join(exclude_words)
    params = {
            'text': f'{language} not {exclude_words} !(разработчик or \
                    программист or инженер or developer or programmer or engineer)',
            'area': area,
            'period': period,
            'page': page,
            'per_page': per_page,
            'search_field': 'name',
    }
    response = requests.get('https://api.hh.ru/vacancies/', params=params)
    response.raise_for_status()

    hh_page_salaries = []
    raw_hh_vacancies = response.json()['items']
    for raw_hh_vacancy in raw_hh_vacancies:
        salary = raw_hh_vacancy['salary']
        if salary:
            vacancy_salary = dict(payment_from=salary['from'],
                                  payment_to=salary['to'],
                                  currency=salary['currency'])
        else:
            vacancy_salary = None
        hh_page_salaries.append(vacancy_salary)
    return hh_page_salaries


def get_hh_all_pages_salaries(language, per_page=100):
    '''HH.RU - get language salaries from all search pages'''
    current_page_index = 0
    hh_all_pages_salaries = []
    current_page_salaries = []
    while True:
        try:
            current_page_salaries = get_hh_page_salaries(language=language,
                                                         page=current_page_index)
        except requests.exceptions.HTTPError:
            print(f'HH.RU - Error occured while loading {language} vacancies...')
            current_page_index += 1
            continue

        hh_all_pages_salaries.extend(current_page_salaries)
        if len(current_page_salaries) < per_page:
            break
        current_page_index += 1
    return hh_all_pages_salaries


def get_superjob_page_salaries(language, api_key, town='Moscow', catalogues="48", page=0, per_page=100,
                               exclude_words=['менеджер', 'консультант', 'продавец',
                                              'поддержки', 'поддержка', 'пользователей',]):
    '''SUPERJOB.RU - get language salaries from search page with number=<page>'''
    today = datetime.date.today()
    date_published_from = (today - datetime.timedelta(days=30))
    date_published_from = int(time.mktime(date_published_from.timetuple()))

    params = {}
    headers = {'X-Api-App-Id': api_key}
    for i, key_word in enumerate(['программист', 'разработчик', 'developer',
                                  'programmer', 'инженер', 'engineer']):
        params[f'keywords[{i}][keys]'] = ','.join([language, key_word,])
        params[f'keywords[{i}][skwc]'] = 'and'
        params[f'keywords[{i}][srws]'] = 4
    params['keywords[6][keys]'] = ','.join(exclude_words)
    params['keywords[6][skwc]'] = 'nein'
    params['catalogues'] = catalogues
    params['date_published_from'] = date_published_from
    params['town'] = town
    params['count'] = per_page
    params['page'] = page

    response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                            params=params, headers=headers)
    response.raise_for_status()

    superjob_page_salaries = []
    raw_vacancies = response.json()['objects']
    for raw_vacancy in raw_vacancies:
        payment_from = raw_vacancy['payment_from']
        payment_to = raw_vacancy['payment_to']
        currency = raw_vacancy['currency']
        vacancy_salary = dict(payment_from=payment_from, payment_to=payment_to,
                              currency=currency)
        superjob_page_salaries.append(vacancy_salary)
    return superjob_page_salaries


def get_superjob_all_pages_salaries(language, api_key, per_page=100):
    '''SUPERJOB.RU - get language salaries from all search pages'''
    current_page_index = 0
    superjob_all_pages_salaries = []
    current_page_salaries = []
    while True:
        try:
            current_page_salaries = get_superjob_page_salaries(language=language,
                                                               api_key=api_key,
                                                               page=current_page_index)
        except requests.exceptions.HTTPError:
            print(f'SUPERJOB.RU - Error occured while loading {language} vacancies...')
            current_page_index += 1
            continue

        superjob_all_pages_salaries.extend(current_page_salaries)
        if len(current_page_salaries) < per_page:
            break
        current_page_index += 1
    return superjob_all_pages_salaries


def main():
    '''Main function implementation'''
    env = Env()
    env.read_env()
    superjob_api_key = env('SUPERJOB_API_KEY')

    languages = (
                'C#', 'Ruby', 'Java', 'C', 'Perl',
                'Objective-C', 'Scala', 'Go', 'C++',
                'PHP', 'Python', 'JavaScript', 'TypeScript',
                'Rust', 'Swift', 'Kotlin', '1с',
                )
    hh_lang_stat = []
    superjob_lang_stat = []

    print(f'\nPrepare job statistics, wait for a while please...\n')
    for language in languages:
        hh_lang_salaries = get_hh_all_pages_salaries(language)
        vacancies_found, vacancies_processed, average_salary = calculate_language_statistics(hh_lang_salaries)
        hh_lang_stat.append(dict(language=language,
                                 vacancies_found=vacancies_found,
                                 vacancies_processed=vacancies_processed,
                                 average_salary=average_salary))

        superjob_lang_salaries = get_superjob_all_pages_salaries(language, api_key=superjob_api_key)
        vacancies_found, vacancies_processed, average_salary = calculate_language_statistics(superjob_lang_salaries)
        superjob_lang_stat.append(dict(language=language,
                                       vacancies_found=vacancies_found,
                                       vacancies_processed=vacancies_processed,
                                       average_salary=average_salary))

    print_language_statistics(hh_lang_stat, 'HeadHunter Moscow')
    print_language_statistics(superjob_lang_stat, 'SuperJob Moscow', limit=5)


if __name__ == '__main__':
    main()
