import allure

import helpers


class TestCreateOrder:
    @allure.title('Можно создать заказ с авторизацией и ингредиентами')
    def test_create_order_with_authorization(self, user, ingredients):
        response = helpers.create_order({'ingredients': ingredients}, user['accessToken'])
        assert response.status_code == 200
        body = response.json()
        assert body['success'] is True
        assert body['name']
        assert isinstance(body['order']['number'], int)

    @allure.title('Можно создать заказ без авторизации')
    def test_create_order_without_authorization(self, ingredients):
        response = helpers.create_order({'ingredients': ingredients})
        assert response.status_code == 200
        body = response.json()
        assert body['success'] is True
        assert body['name']
        assert isinstance(body['order']['number'], int)

    @allure.title('Нельзя создать заказ без ингредиентов')
    def test_create_order_without_ingredients(self, user):
        response = helpers.create_order({'ingredients': []}, user['accessToken'])
        assert response.status_code == 400
        assert response.json() == {
            'success': False,
            'message': 'Ingredient ids must be provided',
        }

    @allure.title('Нельзя создать заказ с неверным хешем ингредиента')
    def test_create_order_with_invalid_ingredient_hash(self, user):
        response = helpers.create_order({'ingredients': ['badhash']}, user['accessToken'])
        assert response.status_code == 500
        assert 'Internal Server Error' in response.text
