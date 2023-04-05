from abc import ABC, abstractmethod
import os
import requests


class Engine(ABC):
    @abstractmethod
    def get_class_vacancies(self, url: str, params: dict) -> dict:
        """Метод для выполнения запроса к сайту и получения данных"""
        pass



class HeadHunterAPI(Engine):
    def __init__(self):
        self.url_hh = "https://api.hh.ru/vacancies"

    def get_class_vacancies(self, exp: str, key_word: str):
        params = {'text': key_word, 'per_page': 100, 'experience': exp, 'area': 113}
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

    def __str__(self):
        return f"title='{self.title}', salary='{self.salary}', " \
               f"description='{self.description}', employer='{self.employer}', url='{self.url}'"


class SuperJobAPI(Engine):
    def __init__(self):
        self.sj_api_key: str = os.getenv('SJ_API_KEY')
        self.headers = {'X-Api-App-Id': self.sj_api_key}
        self.url_sj = "https://api.superjob.ru/2.0/vacancies/"

    def get_class_vacancies(self, exp: str, key_word: str):
        params = {'keyword': {key_word}, 'count': 100, "experience": exp, "currency": {"0":"rub"}}

        response = requests.get(self.url_sj, headers=self.headers, params=params)
        if response.ok:
            data = response.json()
            vacancies_data = data['objects']
            vacancies = []
            for vacancy in vacancies_data:
                title = vacancy['profession']
                try:
                    if vacancy['payment_to'] == 0:  ### Проверка на диапазон зарплаты
                        salary = {'from': vacancy['payment_from'], 'currency': vacancy['currency']}
                    elif vacancy['payment_from'] == 0:
                        salary = {'from': vacancy['payment_to'], 'currency': vacancy['currency']}
                    else:
                        salary = {'from': vacancy['from'], 'to': vacancy['to'],
                                  'currency': vacancy['currency']}
                except:
                    salary = {'from': 0, 'currency': 'rub'}
                description = vacancy['candidat']
                employer = vacancy['firm_name']
                url = vacancy['link']
                vacancy = Vacancy(title, salary, description, employer, url)
                vacancies.append(vacancy)
            return vacancies
        else:
            return []
