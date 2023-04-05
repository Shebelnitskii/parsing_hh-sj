import json
import re
import os


class JSONSaver:
    def __init__(self):
        self.file_name: str = 'JSON.json'

    def add_vacancies(self, headhunter=None, superjob=None):
        """
        Сохраняет информацию о вакансиях в файл JSON.
        """
        if headhunter is not None and superjob is None:
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump(
                    sorted([vars(vacancy) for vacancy in headhunter], key=lambda x: x['salary']['from'], reverse=True),
                    file, ensure_ascii=False, indent=4)
        elif superjob is not None and headhunter is None:
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump(
                    sorted([vars(vacancy) for vacancy in superjob], key=lambda x: x['salary']['from'], reverse=True),
                    file, ensure_ascii=False, indent=4)
        elif headhunter is None and superjob is None:
            print('--------------------------------')
        else:
            with open('JSON_HH.json', 'w', encoding='utf-8') as file:
                json.dump([vars(vacancy) for vacancy in headhunter], file, ensure_ascii=False, indent=4)
            with open('JSON_SJ.json', 'w', encoding='utf-8') as file:
                json.dump([vars(vacancy) for vacancy in superjob], file, ensure_ascii=False, indent=4)
            # Открыть первый файл JSON и прочитать данные
            with open('JSON_HH.json', 'r', encoding='utf-8') as f:
                json_hh = json.load(f)

            # Открыть второй файл JSON и прочитать данные
            with open('JSON_SJ.json', 'r', encoding='utf-8') as f:
                json_sj = json.load(f)
            vacancies = json_hh + json_sj
            sorted_vacancies = sorted(vacancies, key=lambda v: v['salary']['from'], reverse=True)
            with open(self.file_name, 'w', encoding='utf-8') as f:
                json.dump(sorted_vacancies, f, ensure_ascii=False, indent=4)

            # удаляем JSON-файлы
            os.remove("JSON_HH.json")
            os.remove("JSON_SJ.json")

    def clear_json(self):
        """
        Очищает файл JSON.
        """
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump([], file)

    def get_vacancies_by_salary(self, salary_input):
        """
        Возвращает список вакансий с заданной зарплатой.

        :param salary: Зарплата в формате "100 000-150 000 руб."
        :return: Список вакансий.
        """
        with open(self.file_name, 'r', encoding='utf-8') as file:
            vacancy = json.load(file)
        with open(self.file_name, 'w', encoding='utf-8') as file:
            test_dict = []
            try:
                salary, currency = salary_input.split(' ')
                if currency in ['руб', 'RUR', 'rub']:
                    currency = ['руб', 'rur', 'rub', 'RUR']
            except:
                salary = salary_input
                currency = ['руб', 'rur', 'rub', 'RUR']
            for vac in vacancy:
                try:
                    if int(vac['salary']['from']) >= int(salary) and vac['salary']['currency'] in currency:
                        test_dict.append(vac)
                    elif vac['salary']['currency'] in ['usd', 'USD'] and int(vac['salary']['from']) * 75 >= int(salary):
                        test_dict.append(vac)
                except:
                    continue
            json.dump(test_dict, file, ensure_ascii=False, indent=4)

    def search_words(self, search_words):
        if search_words == '':
            with open(self.file_name, 'r', encoding='utf-8') as file:
                vacancies = json.load(file)
            return vacancies
        else:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                vacancies = json.load(file)
            with open(self.file_name, 'w', encoding='utf-8') as file:
                search_dict = []
                words_lower = search_words.lower()
                split_vacancy = re.findall(r'\b\w+\b', words_lower)
                for vac in vacancies:
                    title_lower = str(vac['description']).lower()
                    split_title = re.findall(r'\b\w+\b', title_lower)
                    if set(split_vacancy) & set(split_title):
                        search_dict.append(vac)
                json.dump(search_dict, file, ensure_ascii=False, indent=4)

    def json_results(self):
        with open(self.file_name, 'r', encoding='utf-8') as file:
            final = json.load(file)
            return final
