from abc import ABC,abstractmethod
import json
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

    def get_class_vacancies(self, key: str, top_n: int) -> dict:
        params = {'text': key, 'per_page': top_n}
        response = requests.get(self.url_hh, params=params)
        if response.ok:
            data = response.json()
            vacancies_data = data['items']
            self.vacancies = []
            for vacancy in vacancies_data:
                title = vacancy['name']
                salary_data = vacancy['salary']
                try:
                    if salary_data['to'] == None: ### Проверка на диапазон зарплаты
                        salary = f"{salary_data['from']} {salary_data['currency']}"
                    elif salary_data['from'] == None:
                        salary = f"{salary_data['to']} {salary_data['currency']}"
                    else:
                        salary = f"{salary_data['from']}-{salary_data['to']} {salary_data['currency']}"
                except:
                    salary = f'Информация отсутствует'
                description = vacancy['snippet']['requirement']
                employer = vacancy['employer']['name']
                url = vacancy['alternate_url']
                vacancy = VacancyHH(title, salary, description, employer, url)
                self.vacancies.append(vacancy)
            return self.vacancies
        else:
            self.vacancies = []
            return self.vacancies

class VacancyHH:
    def __init__(self, title, salary, description, employer, url):
        self.title = title
        self.salary = salary
        self.description = description
        self.employer = employer
        self.url = url

    def __repr__(self):
        return f"Vacancy(title='{self.title}', salary='{self.salary}', " \
               f"description='{self.description}', employer='{self.employer}', url='{self.url}')"


# class SuperJobAPI(Engine):
#     def __init__(self):
#         sj_api_key: str = os.getenv('SJ_API_KEY')
#         self.headers = {'X-Api-App-Id': sj_api_key}
#         self.url_sj = "https://api.superjob.ru/2.0/vacancies/"
#
#     def get_request(self, params) -> dict:
#         response = requests.get(self.url_sj, headers=self.headers, params=params)
#         if response.ok:
#             data = response.json()
#         else:
#             data = {}
#         return data

hh_api = HeadHunterAPI()
# search_query = input("Введите поисковый запрос: ")
# top_n = int(input("Введите количество вакансий для вывода в топ N: "))
search_query = 'python'
top_n = 20
hh_vacancies = hh_api.get_class_vacancies(search_query, top_n)
print(len(hh_vacancies))
json_saver = JSONSaver()
json_saver.add_vacancy(hh_vacancies)
# json_saver.get_vacancies_by_salary("50000 RUR")
# json_saver.clear_json()
json_saver.delete_vacancy("РаЗрАботчик,django,c++")




# sj_api= SuperJobAPI()
# params_sj = {'keyword': 'python, junior', 'per_page': 1}
# print(sj_api.get_request(url_sj,params_sj))