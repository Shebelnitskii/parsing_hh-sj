from abc import ABC, abstractmethod

class Engine(ABC):
    @abstractmethod
    def get_class_vacancies(self, url: str, params: dict) -> dict:
        """Метод для выполнения запроса к сайту и получения данных"""
        pass

    @staticmethod
    def get_class_vacancies(self, exp, key_word):
        pass
