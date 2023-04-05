import src.classes
from src.json_saver import JSONSaver


def user_interaction():
    try:
        hh_api, sj_api = check_platform()
        search_query = str(input("Введите поисковый запрос: "))
        try:
            hh_vacancies, sj_vacancies = get_class_by_platform(hh_api, sj_api, search_query)
        except:
            hh_vacancies, sj_vacancies = None, None
        salary_sort = input("Введите минимальную зарплату для поиска(rub): ")
        try:
            if salary_sort.strip() == '':
                salary_sort = 0
                print("Вы не ввели минимальную зарплату")
        except ValueError:
            salary_sort = 0
            print("Некорректное значение. Минимальное значение будет равно 0")
        filter_words = input("Введите ключевые слова для фильтрации вакансий в описании: ")
        output_results(hh_vacancies, sj_vacancies, salary_sort, filter_words)
    except:
        print('До скорой встречи!')


def check_platform():
    print("Введите 'Выход/Exit' чтобы закрыть программу")
    while True:
        platform_input = input('Введите платформы для поиска (HeadHunter\SuperJob): ').lower().split(' ')
        if 'выход' in platform_input or 'exit' in platform_input:
            print('Выход из программы')
            return False
        elif set(platform_input) & {'headhunter', 'hh'} and set(platform_input) & {'superjob', 'sj'}:
            hh_api = src.classes.HeadHunterAPI()
            sj_api = src.classes.SuperJobAPI()
            print('Вы выбрали поиск в HH и SJ')
            return hh_api, sj_api
        # обе платформы
        elif set(platform_input) & {'headhunter', 'hh'}:
            hh_api = src.classes.HeadHunterAPI()
            print('Вы выбрали поиск в HH')
            return hh_api, None
        # только HeadHunter
        elif set(platform_input) & {'superjob', 'sj'}:
            sj_api = src.classes.SuperJobAPI()
            print('Вы выбрали поиск в SJ')
            return None, sj_api
        # только SuperJob
        else:
            print('Вы не ввели платформу')
            continue

def get_class_by_platform(hh_api, sj_api, search_word):
    if hh_api is not None and sj_api is not None:
        hh_vacancies = hh_api.get_class_vacancies(search_word)
        sj_vacancies = sj_api.get_class_vacancies(search_word)
        return hh_vacancies, sj_vacancies
    if sj_api is not None:
        sj_vacancies = sj_api.get_class_vacancies(search_word)
        return None, sj_vacancies
    if hh_api is not None:
        hh_vacancies = hh_api.get_class_vacancies(search_word)
        return hh_vacancies, None

def output_results(hh_vacancies, sj_vacancies, salary_sort, filter_words):
    json_saver = JSONSaver()
    json_saver.add_vacancies(headhunter=hh_vacancies, superjob=sj_vacancies)
    json_saver.get_vacancies_by_salary(salary_sort)
    json_saver.search_words(filter_words)
    final = json_saver.json_results()
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    if len(final) == 0:
        print('Вакансий по вашему запросу нет')
    else:
        for x in range(top_n):
            try:
                text = final[x]['description'].replace('<highlighttext>', '').replace('</highlighttext>', '')
                try:
                    salary_text = f"{final[x]['salary']['from']}-{final[x]['salary']['to']} руб"
                except:
                    salary_text = f"{final[x]['salary']['from']} руб"
                print(f"{final[x]['title']}\nЗарплата: {salary_text}\nОписание вакансии:\n{text}\nСсылка: {final[x]['url']}\n")
            except:
                print('Больше вакансий нет')
                break



user_interaction()
