from terminaltables import AsciiTable


def print_salary_statistics(lang_tab, tab_title, limit=100):
    '''Print salary statistics in a good-looking table'''
    lang_tab_form = [('Язык программирования', 'Вакансий найдено',
                      'Вакансий обработано', 'Средняя зарплата',),]
    lang_tab = sorted(lang_tab, key=lambda tab_line: -tab_line['average_salary'])
    for lang_tab_line in lang_tab:
        lang, vacancy_found, vacancy_proceed, average_salary = lang_tab_line.values()
        if vacancy_found >= limit:
            lang_tab_form.append((lang, vacancy_found,
                                    vacancy_proceed, average_salary,))
    salary_tab_instance = AsciiTable(lang_tab_form, tab_title)
    print(salary_tab_instance.table)


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
