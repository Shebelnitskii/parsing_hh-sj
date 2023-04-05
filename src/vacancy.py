class Vacancy:
    def __init__(self, title, salary, description, url):
        self.title = title ###  Название вакансии
        self.salary = salary ###  Информация о зарплате в виде словаря. Может содержать ключи 'from', 'to' и 'currency'.
        self.description = description ### Описание вакансии
        self.url = url ### Ссылка на вакансию

    def __str__(self):
        """
            Возвращает строковое представление вакансии в формате:
            "название='...', зарплата='...', описание='...', ссылка='...'"
        """
        return f"title='{self.title}', salary='{self.salary}', " \
               f"description='{self.description}', url='{self.url}'"