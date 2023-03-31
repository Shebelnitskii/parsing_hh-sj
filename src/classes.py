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

class HH(Engine):
    def get_request(self, url: str, params: dict) -> dict:
        response = requests.get(url, params=params)
        if response.ok:
            data = response.json()
        else:
            data = {}
        return data

class SuperJob(Engine):
    def __init__(self):
        sj_api_key: str = os.getenv('SJ_API_KEY')
        self.headers = {'X-Api-App-Id': sj_api_key}

    def get_request(self, url: str, params: dict) -> dict:
        response = requests.get(url, headers=self.headers, params=params)
        if response.ok:
            data = response.json()
        else:
            data = {}
        return data

# hh = HH()
# url = "https://api.hh.ru/vacancies"
# params = {'text': 'python', 'per_page': 10}
# print(hh.get_request(url,params))

sj= SuperJob()
url_sj = "https://api.superjob.ru/2.0/vacancies/"
params_sj = {'keyword': 'python', 'per_page': 10}
print(sj.get_request(url_sj,params_sj))