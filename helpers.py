import uuid

import allure
import requests

import data

TIMEOUT = 30


def generate_user():
    suffix = uuid.uuid4().hex[:10]
    return {
        'email': f'julia_{suffix}@yandex.ru',
        'password': 'password',
        'name': 'Julia',
    }


@allure.step('Создать пользователя')
def register_user(payload):
    return requests.post(data.BASE_URL + data.REGISTER, json=payload, timeout=TIMEOUT)


@allure.step('Авторизовать пользователя')
def login_user(email, password):
    return requests.post(
        data.BASE_URL + data.LOGIN,
        json={'email': email, 'password': password},
        timeout=TIMEOUT,
    )


@allure.step('Изменить данные пользователя')
def update_user(payload, token=None):
    headers = None if token is None else {'Authorization': token}
    return requests.patch(
        data.BASE_URL + data.USER,
        json=payload,
        headers=headers,
        timeout=TIMEOUT,
    )


@allure.step('Удалить пользователя')
def delete_user(token):
    return requests.delete(
        data.BASE_URL + data.USER,
        headers={'Authorization': token},
        timeout=TIMEOUT,
    )


@allure.step('Получить список ингредиентов')
def get_ingredients():
    return requests.get(data.BASE_URL + data.INGREDIENTS, timeout=TIMEOUT)


@allure.step('Создать заказ')
def create_order(payload, token=None):
    headers = None if token is None else {'Authorization': token}
    return requests.post(
        data.BASE_URL + data.ORDERS,
        json=payload,
        headers=headers,
        timeout=TIMEOUT,
    )


@allure.step('Получить заказы пользователя')
def get_orders(token=None):
    headers = None if token is None else {'Authorization': token}
    return requests.get(data.BASE_URL + data.ORDERS, headers=headers, timeout=TIMEOUT)


def ingredient_ids():
    ingredients = get_ingredients().json()['data']
    bun_id = next(item['_id'] for item in ingredients if item['type'] == 'bun')
    other_id = next(item['_id'] for item in ingredients if item['type'] != 'bun')
    return [bun_id, other_id]
