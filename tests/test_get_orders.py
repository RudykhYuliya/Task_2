import allure

import helpers


class TestGetOrders:
    @allure.title('Можно получить заказы авторизованного пользователя')
    def test_get_orders_of_authorized_user(self, user, ingredients):
        created = helpers.create_order({'ingredients': ingredients}, user['accessToken'])
        number = created.json()['order']['number']
        response = helpers.get_orders(user['accessToken'])
        assert response.status_code == 200
        body = response.json()
        assert body['success'] is True
        assert number in [order['number'] for order in body['orders']]

    @allure.title('Нельзя получить заказы без авторизации')
    def test_get_orders_without_authorization(self):
        response = helpers.get_orders()
        assert response.status_code == 401
        assert response.json() == {'success': False, 'message': 'You should be authorised'}
