import requests
from environs import Env
from terminaltables import AsciiTable
from agregators.superjob import SuperJobAgregator
from agregators.hh import HeadHunterJobAgregator


env = Env()
env.read_env()
SUPERJOB_API_KEY = env('SUPERJOB_API_KEY')


def print_salary(salary_statistic, table_title, limit=90):
    '''Print salary statistics in a good-looking table'''
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


def main():
    '''Main function implementation'''
    languages = (
                'C#', 'Ruby', 'Java', 'C',
                'Objective-C', 'Scala', 'Go', 'C++',
                'PHP', 'JavaScript', 'TypeScript', 'Python',
                'Rust', 'Swift', 'Cobol', '1с',
                )

    hh_statistics = {}
    superjob_statistics = {}
    print(f'\033[92m\nPrepare job statistics, wait for a while please...\033[0m')
    for language in languages:
        try:
            hh_agregator = HeadHunterJobAgregator(language=language)
            vacancies_found, vacancies_processed, averge_salary = hh_agregator.calculate_average_salary()
            if vacancies_processed > 0:
                hh_statistics[language] = dict(vacancies_found=vacancies_found,
                                               vacancies_processed=vacancies_processed,
                                               average_salary=averge_salary)
        except requests.exceptions.HTTPError:
            print(f'HH.RU - Error occured while load {language} vacancies')

        try:
            superjob_agregator = SuperJobAgregator(superjob_api_key=SUPERJOB_API_KEY, language=language)
            vacancies_found, vacancies_processed, averge_salary = superjob_agregator.calculate_average_salary()
            if vacancies_processed > 0:
                superjob_statistics[language] = dict(vacancies_found=vacancies_found,
                                                     vacancies_processed=vacancies_processed,
                                                     average_salary=averge_salary)
        except requests.exceptions.HTTPError:
            print(f'SUPERJOB.RU - Error occured while load {language} vacancies')
    print_salary(hh_statistics, 'HeadHunter Moscow')
    print_salary(superjob_statistics, 'SuperJob Moscow', limit=5)


if __name__ == '__main__':
    main()
