from src.abstract import Engine
from src.vacancy import Vacancy
import requests

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
