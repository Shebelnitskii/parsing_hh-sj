from src.json_saver import JSONSaver
from src.superjob import SuperJobAPI
from src.headhuner import HeadHunterAPI


def user_interaction():
    """
    Функция, которая осуществляет взаимодействие с пользователем, запрашивая данные для поиска вакансий и вывода результатов
    """
    try:
        hh_api, sj_api = check_platform() ### Получение API для выбранных платформ
        hh_vacancies, sj_vacancies = get_class_by_platform(hh_api, sj_api)  ### Получение вакансий для выбранных платформ
        filter_word_input = filter_words() ### Получение ключевых слов
        salary_input = salary_sort() ### Получение минимальной зарплаты
        output_results(hh_vacancies, sj_vacancies, filter_word_input, salary_input) ### Вывод результатов поиска
    except:
        print('До скорой встречи!')


def check_platform():
    print("Введите 'Выход/Exit' чтобы закрыть программу")
    while True:
        """Цикл while запускает бесконечный цикл ввода пользователем 
        платформ для поиска. Если пользователь вводит 'выход' или 'exit',
        программа закрывается."""
        platform_input = input('Введите платформы для поиска (HeadHunter\SuperJob): ').lower().split(' ')
        if 'выход' in platform_input or 'exit' in platform_input:
            print('Выход из программы')
            raise SystemExit
        ### Если пользователь ввел обе платформы (HeadHunter и SuperJob)
        ### то создаются объекты классов HeadHunterAPI и SuperJobAPI
        elif set(platform_input) & {'headhunter', 'hh'} and set(platform_input) & {'superjob', 'sj'}:
            hh_api = HeadHunterAPI()
            sj_api = SuperJobAPI()
            print('Вы выбрали поиск в HH и SJ')
            return hh_api, sj_api
        elif set(platform_input) & {'headhunter', 'hh'}:
            hh_api = HeadHunterAPI()
            print('Вы выбрали поиск в HH')
            return hh_api, None
        ### только HeadHunter
        elif set(platform_input) & {'superjob', 'sj'}:
            sj_api = SuperJobAPI()
            print('Вы выбрали поиск в SJ')
            return None, sj_api
        ### только SuperJob
        else:
            print('Вы не ввели платформу')
            continue


def get_class_by_platform(hh_api, sj_api):
    """Функция для получения объектов классов API в
    зависимости от выбранных платформ"""

    search_query = str(input("Введите поисковый запрос: "))
    hh_exp, sj_exp = experience_input()  ### # Получение значения опыта работы для HeadHunter API и SuperJob API
    if 'выход' in search_query or 'exit' in search_query:
        print('Выход из программы')  ### # Проверка на выход из программы
        raise SystemExit
    if hh_api is not None and sj_api is not None:
        ### Если выбраны обе платформы, то получаем объекты для каждой
        hh_vacancies = hh_api.get_class_vacancies(hh_exp, search_query)
        sj_vacancies = sj_api.get_class_vacancies(sj_exp, search_query)
        return hh_vacancies, sj_vacancies
    if sj_api is not None:
        ### Если выбран только SuperJob
        sj_vacancies = sj_api.get_class_vacancies(sj_exp, search_query)
        return None, sj_vacancies
    if hh_api is not None:
        ### Если выбран только HeadHunter
        hh_vacancies = hh_api.get_class_vacancies(hh_exp, search_query)
        return hh_vacancies, None


def salary_sort():
    while True:
        salary_min = input("Введите минимальную зарплату для поиска (rub): ")
        if 'выход' in salary_min or 'exit' in salary_min:
            print('Выход из программы')
            raise SystemExit
        if not salary_min.strip():  ### Проверка, что введено значение не пустое Если значение пустое, то возвращается минимальное значение 0.
            print("Вы не ввели минимальную зарплату. Минимальное значение будет равно 0")
            return '0'
        try:
            salary_min = int(salary_min)
            return salary_min
        except ValueError:
            print("Некорректное значение. Минимальное значение будет равно 0")
            return '0'


def filter_words():
    """ Функция запрашивает у пользователя ввод ключевых слов для фильтрации вакансий по
    описанию и возвращает введенные слова или пустую строку, если пользователь ничего не ввел.
    Если введено "выход" или "exit", то программа завершается."""

    words = input(
        "Введите ключевые слова для фильтрации вакансий в описании(чем больше слов тем больше найдётся соответствий):\n")
    if 'выход' in words or 'exit' in words:
        print('Выход из программы')
        raise SystemExit
    elif words == '':
        print('Вы ничего не ввели')
        return words
    else:
        return words


def experience_input():
    """
    Функция позволяет пользователю выбрать требуемый опыт
    работы для вакансии на сайтах HeadHunter и SuperJob.
    """
    hh_experience = ["noExperience", "between1And3", "between3And6", "moreThan6"]
    sj_experience = {"1": "без опыта", "2": "от 1 года", "3": "от 3 лет", "4": "от 6 лет"}
    print("Выберите опыт работы:\n1. Без опыта\n2. От 1 года до 3 лет\n3. От 3 до 6 лет\n4. Более 6 лет")
    choice = input("Введите номер: ")
    if 'выход' in choice or 'exit' in choice:  ### проверяет, если пользователь ввел 'выход' или 'exit', то программа закрывается;
        print('Выход из программы')
        raise SystemExit

    if choice not in ["1", "2", "3",
                      "4"]:  ### проверяет, если пользователь ввел неправильный номер опции, то выбирается значение по умолчанию
        print("Неверный ввод. По умолчанию будет выбран вариант 'без опыта'")
        hh_value = hh_experience[0]
        sj_value = {'1': sj_experience['1']}
        return hh_value, sj_value

    hh_value = hh_experience[int(choice) - 1]
    sj_value = {choice: sj_experience[choice]}
    return hh_value, sj_value


def output_results(hh_vacancies, sj_vacancies, filter_words, salary_input):
    """
    Функция вывода результатов поиска вакансий.
    - hh_vacancies: список вакансий с сайта HeadHunter, полученный из API;
    - sj_vacancies: список вакансий с сайта SuperJob, полученный из API;
    - filter_words: ключевые слова для фильтрации вакансий;
    - salary_input: минимальная зарплата для поиска вакансий.
    """
    json_saver = JSONSaver() ### Создание объекта для сохранения результатов в JSON-файл
    json_saver.add_vacancies(headhunter=hh_vacancies, superjob=sj_vacancies) ### Добавление вакансий
    json_saver.search_words(filter_words) ### Фильтрация вакансий по ключевым словам
    json_saver.get_vacancies_by_salary(salary_input) ### Фильтрация вакансий по зарплате
    final = json_saver.json_results() ### Получение результата в виде словаря
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    print('\n')
    if len(final) == 0: ### Если список вакансий пуст, выводим сообщение об отсутствии результатов
        print('Вакансий по вашему запросу нет')
    else:
        for x in range(top_n): # Цикл для вывода топ N вакансий
            try:
                text = final[x]['description'].replace('<highlighttext>', '').replace('</highlighttext>', '') # Удаление тегов из описания вакансии
                try: ### Обработка зарплаты
                    salary_text = f"Зарплата: {final[x]['salary']['from']}-{final[x]['salary']['to']} руб"
                except: ### Если зарплата не указана, выводим соответствующее сообщение
                    if final[x]['salary']['from'] == 0:
                        salary_text = 'Зарплата не указана'
                    else:
                        salary_text = f"Зарплата: {final[x]['salary']['from']} руб"
                # Вывод названия вакансии, зарплаты, описания вакансии и ссылки на неё
                print(f"{final[x]['title']}\n{salary_text}\nОписание вакансии:\n{text}\nСсылка: {final[x]['url']}\n")
            except:
                # Если вакансий меньше, чем заданное количество, выводим соответствующее сообщение и завершаем цикл
                print('Больше вакансий нет')
                break
