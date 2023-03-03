import requests
from environs import Env
from terminaltables import AsciiTable
from agregators.superjob import SuperJobAgregator
from agregators.hh import HeadHunterJobAgregator


env = Env()
env.read_env()
SUPERJOB_API_KEY = env('SUPERJOB_API_KEY')


def print_salary(salary_statistic, table_title, limit=100):
    '''Print salary statistics in a good-looking table'''
    table_title = table_title
    table_header = ('Язык программирования', 'Вакансий найдено',
                    'Вакансий обработано', 'Средняя зарплата',)
    table_form = []
    table_lines = []
    for language in salary_statistic.keys():
        salary_params = salary_statistic[language]
        vacancies_found = salary_params['vacancies_found']
        if vacancies_found < limit:
            continue

        vacancies_processed = salary_params['vacancies_processed']
        average_salary = salary_params['average_salary']
        table_lines.append((language, vacancies_found,
                            vacancies_processed, average_salary,))

    table_lines = sorted(table_lines,
                         key=lambda lang_statistic: lang_statistic[3],
                         reverse=True)
    table_form.append(table_header)
    table_form += table_lines

    TABLE_DATA = tuple(table_form)
    table_instance = AsciiTable(TABLE_DATA, table_title)
    table_instance.justify_columns[2] = 'right'
    print()
    print(table_instance.table)


def grab_superjob(languages):
    '''Grab vacancies from superjob.ru to calculate programmers salaries'''
    superjob_statistics = {}
    for language in languages:
        print(f'SJ.RU - Proceeding language - {language}...')
        try:
            agregator = SuperJobAgregator(superjob_api_key=SUPERJOB_API_KEY,
                                          language=language)
        except requests.exceptions.HTTPError:
            print(f'Error occured while load {language} vacancies')
            continue
        vacancies_found, vacancies_processed, averge_salary = agregator.calculate_average_salary()
        if vacancies_processed > 0:
            superjob_statistics[language] = dict(vacancies_found=vacancies_found,
                                                 vacancies_processed=vacancies_processed,
                                                 average_salary=averge_salary
                                                 )
    return superjob_statistics


def grab_hhjob(languages):
    '''Grab vacancies from hh.ru to calculate programmers salaries'''
    hh_statistics = {}
    for language in languages:
        print(f'HH.RU - Proceeding language - {language}...')
        try:
            agregator = HeadHunterJobAgregator(language=language)
        except requests.exceptions.HTTPError:
            print(f'Error occured while load {language} vacancies')
            continue
        vacancies_found, vacancies_processed, averge_salary = agregator.calculate_average_salary()
        if vacancies_processed > 0:
            hh_statistics[language] = dict(vacancies_found=vacancies_found,
                                           vacancies_processed=vacancies_processed,
                                           average_salary=averge_salary
                                           )
    return hh_statistics


def main():
    '''Main function implementation'''
    languages = (
                'C#',
                'Ruby',
                'Java',
                'C',
                'Objective-C',
                'Scala',
                'Go',
                'C++',
                'PHP',
                'JavaScript',
                'TypeScript',
                'Python',
                'Rust',
                'Swift',
                'Cobol',
                '1с',
                 )
    hh_statistics = grab_hhjob(languages)
    print_salary(hh_statistics, 'HeadHunter Moscow')

    superjob_statistics = grab_superjob(languages)
    print_salary(superjob_statistics, 'SuperJob Moscow', limit=5)


if __name__ == '__main__':
    main()
