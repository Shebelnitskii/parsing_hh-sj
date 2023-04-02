import json
import re
class JSONSaver:
    def __init__(self):
        self.file_name: str = 'JSON_HH'
        self.vacancies = []
    def add_vacancy(self, vacancies):
        """
        Сохраняет информацию о вакансиях в файл JSON.

        :param vacancies: Список экземпляров класса VacancyHH.
        :param file_name: Имя файла для сохранения.
        """
        self.vacancies = vacancies
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump([vars(vacancy) for vacancy in vacancies], file, ensure_ascii=False, indent=4)


    def clear_json(self):
        """
        Очищает файл JSON.
        """
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump('', file, ensure_ascii=False, indent=4)

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
                    if '-' in vac['salary']:
                        salary_split = vac['salary'].split('-')
                        if int(salary) <= int(salary_split[0]):
                            test_dict.append(vac)
                    else:
                        salary_split = vac['salary'].split()
                        if int(salary) <= int(salary_split[0]):
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