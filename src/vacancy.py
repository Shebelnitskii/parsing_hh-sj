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