from abc import ABC,abstractmethod
import os
import requests

class Engine(ABC):
    @abstractmethod
    def get_request(self, url: str, params: dict) -> dict:
        """Метод для выполнения запроса к сайту и получения данных"""
        pass

    @staticmethod
    def get_connector(file_name: str):
        """Метод для получения экземпляра класса Connector"""
        pass

class HeadHunterAPI(Engine):
    def __init__(self):
        self.url_hh = "https://api.hh.ru/vacancies"

    def get_request(self, key: str) -> dict:
        self.params = {'text': key, 'per_page': 10}
        response = requests.get(self.url_hh, params=self.params)
        if response.ok:
            data = response.json()
            vacancies_data = data['items']
            return vacancies_data
        else:
            vacancies_data = []
            return vacancies_data

    def get_class_vacancies(self, key):
        vacancies = []
        for vacancy in self.get_request(key):
            title = vacancy.get('name', '')
            salary_data = vacancy.get('salary', {})
            salary = f"{salary_data.get('from', '')}-{salary_data.get('to', '')} {salary_data.get('currency', '')}"
            description = vacancy.get('snippet', {}).get('requirement', '')
            employer = vacancy.get('employer', {}).get('name', '')
            url = vacancy.get('alternate_url', {})
            vacancy = VacancyHH(title=title, salary=salary, description=description, employer=employer, url=url)
            vacancies.append(vacancy)
        return vacancies


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
# find_key_hh:str = input("Введите ключ-поиск:\n")
find_key_hh = 'python'
# params = {'text': 'python', 'per_page': 1}
hh_dict_class_vacancies = hh_api.get_class_vacancies(find_key_hh)
print(hh_dict_class_vacancies[0])




# sj_api= SuperJobAPI()
# params_sj = {'keyword': 'python, junior', 'per_page': 1}
# print(sj_api.get_request(url_sj,params_sj))