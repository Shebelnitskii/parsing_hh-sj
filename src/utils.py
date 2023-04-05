import src.abstract
from src.json_saver import JSONSaver
from src.superjob import SuperJobAPI
from src.headhuner import HeadHunterAPI


def user_interaction():
    try:
        hh_api, sj_api = check_platform()
        hh_vacancies, sj_vacancies = get_class_by_platform(hh_api, sj_api)
        filter_word_input = filter_words()
        salary_input = salary_sort()
        output_results(hh_vacancies, sj_vacancies, filter_word_input, salary_input)
    except:
        print('До скорой встречи!')


def check_platform():
    print("Введите 'Выход/Exit' чтобы закрыть программу")
    while True:
        platform_input = input('Введите платформы для поиска (HeadHunter\SuperJob): ').lower().split(' ')
        if 'выход' in platform_input or 'exit' in platform_input:
            print('Выход из программы')
            raise SystemExit
        elif set(platform_input) & {'headhunter', 'hh'} and set(platform_input) & {'superjob', 'sj'}:
            hh_api = HeadHunterAPI()
            sj_api = SuperJobAPI()
            print('Вы выбрали поиск в HH и SJ')
            return hh_api, sj_api
        # обе платформы
        elif set(platform_input) & {'headhunter', 'hh'}:
            hh_api = HeadHunterAPI()
            print('Вы выбрали поиск в HH')
            return hh_api, None
        # только HeadHunter
        elif set(platform_input) & {'superjob', 'sj'}:
            sj_api = SuperJobAPI()
            print('Вы выбрали поиск в SJ')
            return None, sj_api
        # только SuperJob
        else:
            print('Вы не ввели платформу')
            continue


def get_class_by_platform(hh_api, sj_api):
    search_query = str(input("Введите поисковый запрос: "))
    hh_exp, sj_exp = experience_input()
    if 'выход' in search_query or 'exit' in search_query:
        print('Выход из программы')
        raise SystemExit
    if hh_api is not None and sj_api is not None:
        hh_vacancies = hh_api.get_class_vacancies(hh_exp, search_query)
        sj_vacancies = sj_api.get_class_vacancies(sj_exp, search_query)
        return hh_vacancies, sj_vacancies
    if sj_api is not None:
        sj_vacancies = sj_api.get_class_vacancies(sj_exp, search_query)
        return None, sj_vacancies
    if hh_api is not None:
        hh_vacancies = hh_api.get_class_vacancies(hh_exp, search_query)
        return hh_vacancies, None


def salary_sort():
    while True:
        salary_min = input("Введите минимальную зарплату для поиска (rub): ")
        if 'выход' in salary_min or 'exit' in salary_min:
            print('Выход из программы')
            raise SystemExit
        if not salary_min.strip():
            print("Вы не ввели минимальную зарплату. Минимальное значение будет равно 0")
            return '0'
        try:
            salary_min = int(salary_min)
            return salary_min
        except ValueError:
            print("Некорректное значение. Минимальное значение будет равно 0")
            return '0'


def filter_words():
    words = input(
        "Введите ключевые слова для фильтрации вакансий в описании(чем больше слов тем больше найдётся соответствий):\n")
    if 'выход' in words or 'exit' in words:
        print('Выход из программы')
        raise SystemExit
    elif words == '':
        print('Вы не ввели никаких слов')
        return words
    else:
        return words


def experience_input():
    hh_experience = ["noExperience", "between1And3", "between3And6", "moreThan6"]
    sj_experience = {"1": "без опыта", "2": "от 1 года", "3": "от 3 лет", "4": "от 6 лет"}
    print("Выберите опыт работы:\n1. Без опыта\n2. От 1 года до 3 лет\n3. От 3 до 6 лет\n4. Более 6 лет")
    choice = input("Введите номер: ")
    if 'выход' in choice or 'exit' in choice:
        print('Выход из программы')
        raise SystemExit

    if choice not in ["1", "2", "3", "4"]:
        print("Неверный ввод. По умолчанию будет выбран вариант 'без опыта'")
        hh_value = hh_experience[0]
        sj_value = {'1': sj_experience['1']}
        return hh_value, sj_value

    hh_value = hh_experience[int(choice)-1]
    sj_value = {choice: sj_experience[choice]}
    return hh_value, sj_value

def output_results(hh_vacancies, sj_vacancies, filter_words, salary_input):
    json_saver = JSONSaver()
    json_saver.add_vacancies(headhunter=hh_vacancies, superjob=sj_vacancies)
    json_saver.search_words(filter_words)
    json_saver.get_vacancies_by_salary(salary_input)
    final = json_saver.json_results()
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    print('\n')
    if len(final) == 0:
        print('Вакансий по вашему запросу нет')
    else:
        for x in range(top_n):
            try:
                text = final[x]['description'].replace('<highlighttext>', '').replace('</highlighttext>', '')
                try:
                    salary_text = f"Зарплата: {final[x]['salary']['from']}-{final[x]['salary']['to']} руб"
                except:
                    if final[x]['salary']['from'] == 0:
                        salary_text = 'Зарплата не указана'
                    else:
                        salary_text = f"Зарплата: {final[x]['salary']['from']} руб"
                print(f"{final[x]['title']}\n{salary_text}\nОписание вакансии:\n{text}\nСсылка: {final[x]['url']}\n")
            except:
                print('Больше вакансий нет')
                break
