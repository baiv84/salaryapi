from terminaltables import AsciiTable


def print_language_statistics(languages_stat_table, table_title, limit=100):
    '''Print salary statistics in a good-looking table'''
    lang_tab_form = [('Язык программирования', 'Вакансий найдено',
                      'Вакансий обработано', 'Средняя зарплата',),]
    languages_stat_table = sorted(languages_stat_table, key=lambda tab_line: -tab_line['average_salary'])
    for lang_tab_line in languages_stat_table:
        lang, vacancy_found, vacancy_proceed, average_salary = lang_tab_line.values()
        if vacancy_found >= limit:
            lang_tab_form.append((lang, vacancy_found,
                                  vacancy_proceed, average_salary,))
    lang_tab_instance = AsciiTable(lang_tab_form, table_title)
    print(lang_tab_instance.table)


def predict_rub_salary(vacancy):
    '''Calculate average salary for particular vacancy'''
    if not vacancy:
        return None
    payment_from, payment_to, currency = vacancy.values()
    if ((not payment_from) and (not payment_to)) or \
       ((currency != 'RUR') and (currency != 'rub')):
        return None
    elif (payment_from) and (not payment_to):
        return int(payment_from * 1.2)
    elif (payment_to) and (not payment_from):
        return int(payment_to * 0.8)
    return int((payment_from + payment_to) // 2)


def calculate_language_statistics(vacancies_found):
    '''Calculate language salary statistics
       based on found vacancies'''
    average_salary = 0
    vacancies_processed = []
    for vacancy in vacancies_found:
        salary = predict_rub_salary(vacancy)
        if salary:
            vacancies_processed.append(salary)
    vacancies_found_count = len(vacancies_found)
    vacancies_processed_count = len(vacancies_processed)

    if vacancies_processed_count > 0:
        average_salary = sum(vacancies_processed) // vacancies_processed_count
    return (vacancies_found_count, vacancies_processed_count, average_salary,)
