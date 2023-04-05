import json
import re
import os


class JSONSaver:
    def __init__(self):
        self.file_name: str = 'JSON.json'

    def add_vacancies(self, headhunter=None, superjob=None):
        """
        Сохраняет информацию о вакансиях в файл JSON.

        Аргументы:
        headhunter: Список вакансий с сайта HeadHunter.
        superjob: Список вакансий с сайта SuperJob.
        """
        if headhunter is not None and superjob is None: ### Проверка на получение аргумента, если получен только один аргумент то выполняется сохранение словаря в json
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump(
                    sorted([vars(vacancy) for vacancy in headhunter], key=lambda x: x['salary']['from'], reverse=True),
                    file, ensure_ascii=False, indent=4)
        elif superjob is not None and headhunter is None:
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump(
                    sorted([vars(vacancy) for vacancy in superjob], key=lambda x: x['salary']['from'], reverse=True),
                    file, ensure_ascii=False, indent=4)
        elif headhunter is None and superjob is None:
            print('')
        else:
            """При получении двух аргументов для каждого создаётся свой json файл и сохранение в 
            каждый словарь с их API. В дальнейшем словари складываются,сортируются по зарплате и 
            сохраняются в общий json, а временные файлы удаляются
            """
            with open('JSON_HH.json', 'w', encoding='utf-8') as file:
                json.dump([vars(vacancy) for vacancy in headhunter], file, ensure_ascii=False, indent=4)
            with open('JSON_SJ.json', 'w', encoding='utf-8') as file:
                json.dump([vars(vacancy) for vacancy in superjob], file, ensure_ascii=False, indent=4)
            # Открыть первый файл JSON и сохранить данные
            with open('JSON_HH.json', 'r', encoding='utf-8') as f:
                json_hh = json.load(f)
            # Открыть второй файл JSON и сохранить данные
            with open('JSON_SJ.json', 'r', encoding='utf-8') as f:
                json_sj = json.load(f)

            vacancies = json_hh + json_sj ### Сложение двух словарей

            """Перед сохранением в общий json происходит сортировка по зарплате(в начале словаря самое большое значение)"""
            sorted_vacancies = sorted(vacancies, key=lambda v: v['salary']['from'], reverse=True)
            with open(self.file_name, 'w', encoding='utf-8') as f:
                json.dump(sorted_vacancies, f, ensure_ascii=False, indent=4)

            # удаляем JSON-файлы
            os.remove("JSON_HH.json")
            os.remove("JSON_SJ.json")

    def get_vacancies_by_salary(self, salary_input):
        """
        Возвращает список вакансий с заданной зарплатой.

        salary Зарплата в формате "100 000-150 000 руб."
        Список вакансий.
        """
        with open(self.file_name, 'r', encoding='utf-8') as file:
            vacancy = json.load(file)
        with open(self.file_name, 'w', encoding='utf-8') as file:
            test_dict = []
            """Здесь учитывается возможность, что зарплата может быть в долларах,
            но параметры для сайтов hh и sj были добавлены с учетом регионального поиска по РФ
            и зарплате в рублях(уже после написания кода) поэтому проверку по валюте я оставил.
             """
            try:
                salary, currency = salary_input.split(' ') ### разбитие строки на зарплату и валюту
                if currency in ['руб', 'RUR', 'rub']: ### проверка на валюту, в словарях hh и sj валюта указывается по разному
                    currency = ['руб', 'rur', 'rub', 'RUR'] ### по этому сохранение идёт в список(возможных вариантов)
            except: ### если пользователь ввёл только число, валюта автоматически сохраняется в список
                salary = salary_input
                currency = ['руб', 'rur', 'rub', 'RUR']
            for vac in vacancy:
                try:
                    """Проверка, что зарплата отвечает заданным требованиям и 
                        валюта соответствует списку разрешенных валют.
                    """
                    if int(vac['salary']['from']) >= int(salary) and vac['salary']['currency'] in currency:
                        test_dict.append(vac)

                    elif vac['salary']['currency'] in ['usd', 'USD'] and int(vac['salary']['from']) * 75 >= int(salary):
                        test_dict.append(vac) ### Добавление вакансии в список вакансий с требуемой зарплатой.
                except:
                    continue
            json.dump(test_dict, file, ensure_ascii=False, indent=4)

    def search_words(self, search_words):
        ### Если поисковой запрос пустой, возвращает все вакансии из файла
        if search_words == '':
            with open(self.file_name, 'r', encoding='utf-8') as file:
                vacancies = json.load(file)
            return vacancies
        else:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                vacancies = json.load(file)
            ### Иначе происходит поиск вакансий по ключевым словам
            with open(self.file_name, 'w', encoding='utf-8') as file:
                search_dict = []
                words_lower = search_words.lower()  ### Приведение запроса и заголовков вакансий к нижнему регистру
                split_vacancy = re.findall(r'\b\w+\b', words_lower) ### Разбиение запроса и заголовков на отдельные слова
                for vac in vacancies: ### Поиск совпадений между словами запроса и описанием вакансий
                    title_lower = str(vac['description']).lower()
                    split_title = re.findall(r'\b\w+\b', title_lower)
                    if set(split_vacancy) & set(split_title):
                        search_dict.append(vac)
                ### Сохранение найденных вакансий в файл
                json.dump(search_dict, file, ensure_ascii=False, indent=4)

    def json_results(self):
        ''' Вывод итоговой информации по файлу json '''
        with open(self.file_name, 'r', encoding='utf-8') as file:
            final = json.load(file)
            return final
