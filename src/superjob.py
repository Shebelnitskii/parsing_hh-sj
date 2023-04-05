import os
import requests
from src.abstract import Engine
from src.vacancy import Vacancy

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