from src.abstract import Engine
from src.vacancy import Vacancy
import requests

class HeadHunterAPI(Engine):
    def __init__(self):
        self.url_hh = "https://api.hh.ru/vacancies" # URL API HeadHunter

    def get_class_vacancies(self, exp: str, key_word: str):
        """
        Метод для получения вакансий с помощью API SuperJob.

        exp Опыт работы.
        key_word Ключевое слово для поиска вакансии.
        return Список объектов класса Vacancy.
        """
        params = {'text': key_word, 'per_page': 100, 'experience': exp, 'area': 113}
        response = requests.get(self.url_hh, params=params)
        if response.ok:
            data = response.json()
            vacancies_data = data['items']
            vacancies = []
            for vacancy in vacancies_data:
                title = vacancy['name'] ### Название вакансии
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
                    salary = {'from': 0, 'currency': 'RUR'} ### Если зарплата не указано то в значение фром сохраняется нулевое значение
                description = vacancy['snippet']['requirement']  ### Описание вакансии
                url = vacancy['alternate_url'] ### url ссылка на вакансию
                vacancy = Vacancy(title, salary, description, url)
                vacancies.append(vacancy)
            return vacancies
        else:
            vacancies = []
            return vacancies
