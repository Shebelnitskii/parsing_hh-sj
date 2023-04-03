import json
import re
import os


class JSONSaver:
    def __init__(self):
        self.file_name: str = 'JSON.json'

    def add_vacancy(self, vacanciesHH=None, vacanciesSJ=None):
        """
        Сохраняет информацию о вакансиях в файл JSON.
        """
        if vacanciesHH is None and vacanciesSJ is None:
            print("Введите хотя бы одно значение")
        elif vacanciesHH is not None and vacanciesSJ is None:
            with open('JSON_HH.json', 'w', encoding='utf-8') as file:
                json.dump(
                    sorted([vars(vacancy) for vacancy in vacanciesHH], key=lambda x: x['salary']['from'], reverse=True),
                    file, ensure_ascii=False, indent=4)
        elif vacanciesSJ is not None and vacanciesHH is None:
            with open('JSON_SJ.json', 'w', encoding='utf-8') as file:
                json.dump(
                    sorted([vars(vacancy) for vacancy in vacanciesSJ], key=lambda x: x['salary']['from'], reverse=True),
                    file, ensure_ascii=False, indent=4)
        else:
            with open('JSON_HH.json', 'w', encoding='utf-8') as file:
                json.dump([vars(vacancy) for vacancy in vacanciesHH], file, ensure_ascii=False, indent=4)
            with open('JSON_SJ.json', 'w', encoding='utf-8') as file:
                json.dump([vars(vacancy) for vacancy in vacanciesSJ], file, ensure_ascii=False, indent=4)
            # Открыть первый файл JSON и прочитать данные
            with open('JSON_HH.json', 'r', encoding='utf-8') as f:
                json_hh = json.load(f)

            # Открыть второй файл JSON и прочитать данные
            with open('JSON_SJ.json', 'r', encoding='utf-8') as f:
                json_sj = json.load(f)
            vacancies = json_hh + json_sj
            with open(self.file_name, 'w', encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=4)

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
            salary, currency = salary_input.split(' ')
            for vac in vacancy:
                try:
                    if int(vac['salary']['from']) >= int(salary) and str(vac['salary']['currency']) in ['RUR', 'rub']:
                        test_dict.append(vac)
                    elif vac['salary']['currency'].lower() in ['usd', 'USD']:
                        test_dict.append(vac)
                except:
                    continue
            json.dump(test_dict, file, ensure_ascii=False, indent=4)

    def delete_vacancy(self, vacancy):
        """
        Удаляет вакансию из файла JSON.

        :param vacancy: Экземпляр класса VacancyHH.
        """
        with open(self.file_name, 'r', encoding='utf-8') as file:
            vacancies = json.load(file)
        with open(self.file_name, 'w', encoding='utf-8') as file:
            test_dict = []
            vacancy_lower = vacancy.lower()
            split_vacancy = re.findall(r'\b\w+\b', vacancy_lower)
            for vac in vacancies:
                title_lower = vac['title'].lower()
                split_title = re.findall(r'\b\w+\b', title_lower)
                if set(split_vacancy) & set(split_title):
                    continue
                else:
                    test_dict.append(vac)
            json.dump(test_dict, file, ensure_ascii=False, indent=4)
