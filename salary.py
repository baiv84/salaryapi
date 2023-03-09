import time
import datetime
import requests
from environs import Env
from common import predict_rub_salary
from common import print_salary_statistics


def get_hh_page(language, area=1, period=30, page=0, per_page=100,
                exclude_words=['менеджер', 'консультант', 'продавец',
                               'поддержки', 'поддержка', 'пользователей',]):
    '''Extract salaries from hh.ru search page with number=<page>'''
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
    try:
        response = requests.get('https://api.hh.ru/vacancies/', params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f'HH.RU - Error occured while loading {language} vacancies')
        return []

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


def get_superjob_page(language, town='Moscow', catalogues="48", page=0, per_page=100,
                      exclude_words=['менеджер', 'консультант', 'продавец',
                                     'поддержки', 'поддержка', 'пользователей',]):
    '''Extract salaries from superjob.ru search page with <num>=page'''
    env = Env()
    api_key = env('SUPERJOB_API_KEY')

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

    try:
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f'SUPERJOB.RU - Error occured while loading {language} vacancies')
        return []
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


def get_all_pages_salaries(language, page_func=get_hh_page, per_page=100):
    '''Get salaries from all pages calling <page_func>'''
    current_page_index = 0
    all_pages_salaries = []
    current_page_salaries = []
    while True:
        current_page_salaries = page_func(language=language,
                                          page=current_page_index)
        all_pages_salaries.extend(current_page_salaries)
        if len(current_page_salaries) < per_page:
            break
        current_page_index += 1
    return all_pages_salaries


def get_salary_statistics(language, mode='headhunter'):
    '''Collect language salary statistic from
        particular data sources - hh.ru | superjob.ru'''
    page_func_modes = {
        'headhunter': get_hh_page,
        'superjob': get_superjob_page,
    }

    average_salary = 0
    vacancies_processed = []
    if mode not in page_func_modes:
        mode = 'headhunter'

    vacancies_found = get_all_pages_salaries(language, page_func=page_func_modes[mode])
    for vacancy in vacancies_found:
        salary = predict_rub_salary(vacancy)
        if salary:
            vacancies_processed.append(salary)

    vacancies_found_count = len(vacancies_found)
    vacancies_processed_count = len(vacancies_processed)
    if vacancies_processed_count > 0:
        average_salary = sum(vacancies_processed) // vacancies_processed_count
    return (vacancies_found_count, vacancies_processed_count, average_salary,)


def main():
    '''Main function implementation'''
    env = Env()
    env.read_env()

    languages = (
                'C#', 'Ruby', 'Java', 'C', 'Perl',
                'Objective-C', 'Scala', 'Go', 'C++',
                'PHP', 'Python', 'JavaScript', 'TypeScript',
                'Rust', 'Swift', 'Kotlin', '1с',
                )
    hh_lang_statistic = []
    superjob_lang_statistic = []

    print(f'\nPrepare job statistics, wait for a while please...\n')
    for language in languages:
        vacancies_found, vacancies_processed, average_salary = get_salary_statistics(language, mode='headhunter')
        hh_lang_statistic.append(dict(language=language,
                                      vacancies_found=vacancies_found,
                                      vacancies_processed=vacancies_processed,
                                      average_salary=average_salary))

        vacancies_found, vacancies_processed, average_salary = get_salary_statistics(language, mode='superjob')
        superjob_lang_statistic.append(dict(language=language,
                                            vacancies_found=vacancies_found,
                                            vacancies_processed=vacancies_processed,
                                            average_salary=average_salary))
    print_salary_statistics(hh_lang_statistic, 'HeadHunter Moscow')
    print_salary_statistics(superjob_lang_statistic, 'SuperJob Moscow', limit=5)


if __name__ == '__main__':
    main()
