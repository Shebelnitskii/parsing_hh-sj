from abc import ABC, abstractmethod
import os
import requests
from src.json_saver import JSONSaver


class Engine(ABC):
    @abstractmethod
    def get_class_vacancies(self, url: str, params: dict) -> dict:
        """Метод для выполнения запроса к сайту и получения данных"""
        pass

    @staticmethod
    def get_connector(file_name: str):
        """Метод для получения экземпляра класса Connector"""
        pass


class HeadHunterAPI(Engine):
    def __init__(self):
        self.url_hh = "https://api.hh.ru/vacancies"

    def get_class_vacancies(self, key: str, top_n: int):
        params = {'text': key, 'per_page': top_n, 'experience': 'noExperience'}
        response = requests.get(self.url_hh, params=params)
        if response.ok:
            data = response.json()
            vacancies_data = data['items']
            vacancies = []
            for vacancy in vacancies_data:
                title = vacancy['name']
                salary_data = vacancy['salary']
                try:
                    if salary_data['to'] == None:  ### Проверка на диапазон зарплаты
                        salary = {'from': salary_data['from'], 'currency': salary_data['currency']}
                    elif salary_data['from'] == None:
                        salary = {'from': salary_data['to'], 'currency': salary_data['currency']}
                    else:
                        salary = {'from': salary_data['from'], 'to': salary_data['to'],
                                  'currency': salary_data['currency']}
                except:
                    salary = {'from': 0, 'currency': 'RUR'}
                description = vacancy['snippet']['requirement']
                employer = vacancy['employer']['name']
                url = vacancy['alternate_url']
                vacancy = Vacancy(title, salary, description, employer, url)
                vacancies.append(vacancy)
            return vacancies
        else:
            vacancies = []
            return vacancies


class Vacancy:
    def __init__(self, title, salary, description, employer, url):
        self.title = title
        self.salary = salary
        self.description = description
        self.employer = employer
        self.url = url

    def __repr__(self):
        return f"title='{self.title}', salary='{self.salary}', " \
               f"description='{self.description}', employer='{self.employer}', url='{self.url}'"


class SuperJobAPI(Engine):
    def __init__(self):
        sj_api_key: str = os.getenv('SJ_API_KEY')
        self.headers = {'X-Api-App-Id': sj_api_key}
        self.url_sj = "https://api.superjob.ru/2.0/vacancies/"

    def get_class_vacancies(self, params: dict) -> list:
        response = requests.get(self.url_sj, headers=self.headers, params=params)
        if response.ok:
            data = response.json()
            vacancies_data = data['objects']
            vacancies = []
            for vacancy in vacancies_data:
                title = vacancy['profession']
                salary_data = vacancy['payment_from'] or vacancy['payment_to']
                if salary_data:
                    salary = {'from': vacancy['payment_from'], 'to': vacancy['payment_to'],
                              'currency': vacancy['currency']}
                else:
                    salary = {'from': None, 'to': None, 'currency': None}
                description = vacancy['candidat']
                employer = vacancy['firm_name']
                url = vacancy['link']
                vacancy = Vacancy(title, salary, description, employer, url)
                vacancies.append(vacancy)
            return vacancies
        else:
            return []


# hh_api = HeadHunterAPI()
# search_query = input("Введите поисковый запрос: ")
# top_n = int(input("Введите количество вакансий для вывода в топ N: "))
# search_query = 'python'
# top_n = 100
# hh_vacancies = hh_api.get_class_vacancies(search_query, top_n)
# print(len(hh_vacancies))
# json_saver = JSONSaver()
# json_saver.add_vacancy(hh_vacancies)
# json_saver.get_vacancies_by_salary("50000 RUR")
# json_saver.delete_vacancy("JavaScript, Java")
# with open('JSON_HH', 'r', encoding='utf-8') as file:
#     vacancies = json.load(file)
# print(len(vacancies))
# json_saver.clear_json()
# with open('JSON_HH', 'r', encoding='utf-8') as file:
#     vacancies = json.load(file)
# print(len(vacancies))


sj_api = SuperJobAPI()
params_sj = {'keyword': 'разработчик python', 'count': 1, 'experience': {'1': 'без опыта'}}
print(sj_api.get_class_vacancies(params_sj))
sj_vacancies = sj_api.get_class_vacancies(params_sj)
json_saver = JSONSaver()
json_saver.add_vacancy(sj_vacancies)
print(len(sj_vacancies))
