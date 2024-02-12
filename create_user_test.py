import sender_stand_request
import data
def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body

def positive_assert(first_name):
    # В переменную user_body сохраняется обновленное тело запроса
    user_body = get_user_body(first_name)
            # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)
            # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
            # Проверяется, что в ответе есть поле authToken, и оно не пустое
    assert user_response.json()["authToken"] != ""
            # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()
            # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
                       + user_body["address"] + ",,," + user_response.json()["authToken"]
            # Проверка, что такой пользователь есть, и он единственный
    assert users_table_response.text.count(str_user) == 1

def negative_assert_symbol(first_name):
    # В переменную user_body сохраняется обновленное тело запроса
    user_body = get_user_body(first_name)
            # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)
            # Проверяется, что код ответа равен 201
    assert user_response.status_code == 400

    assert user_response.json()["code"] == 400
    assert user_response.json()['message'] == "Имя пользователя введено некорректно. Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"

def negative_assert_no_first_name(user_body):
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()['message'] == "Не все необходимые параметры были переданы"


def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")

def test_3():
    negative_assert_symbol('A')

def test_4():
    negative_assert_symbol('Аааааааааааааааа')

def test_5():
        positive_assert("QWErty")


def test_6():
    positive_assert("Мария")
def test_7():
    negative_assert_symbol('Человек и Ко')

def test_8():
        negative_assert_symbol('№%@')


def test_9():
    negative_assert_symbol('123')

def test_10():
    user_body = data.user_body.copy()
    user_body.pop('firstName')
    negative_assert_no_first_name(user_body)

# Тест 11. Ошибка
# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)

def test_create_user_number_type_first_name_get_error_response():
        # В переменную user_body сохраняется обновлённое тело запроса
        user_body = get_user_body(12)
        # В переменную user_response сохраняется результат запроса на создание пользователя:
        response = sender_stand_request.post_new_user(user_body)

        # Проверка кода ответа
        assert response.status_code == 400