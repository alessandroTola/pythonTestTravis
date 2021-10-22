import json

from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()  # We need to call the super class setUp method to initialize app and context
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth', data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-type': 'application/json'})
                aut_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {aut_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')
                self.assertEqual(response.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(response.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()
                response = client.get('/item/test_item', headers={'Authorization': self.access_token})

                self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()
                expected = {'message': 'Item deleted'}

                response = client.delete('/item/test_item')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                expected = {'name': 'test_item', 'price': 19.90}
                response = client.post('/item/test_item', data={'price': 19.90, 'store_id': 1})
                self.assertEqual(response.status_code, 201)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 19.90, 1).save_to_db()
                expected = {'message': "An item with name 'test_item' already exists."}

                response = client.post('/item/test_item', data={'price': 19.90, 'store_id': 1})
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                expected = {'name': 'test_item', 'price': 19.90}

                response = client.put('/item/test_item', data={'price': 19.90, 'store_id': 1})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test_item').price, 19.90)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 19.90, 1).save_to_db()
                expected = {'name': 'test_item', 'price': 15.90}

                self.assertEqual(ItemModel.find_by_name('test_item').price, 19.90)

                response = client.put('/item/test_item', data={'price': 15.90, 'store_id': 1})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test_item').price, 15.90)
                self.assertDictEqual(expected, json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 19.90, 1).save_to_db()
                expected = {'items': [{'name': 'test_item', 'price': 19.90}]}

                response = client.get('/items')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(expected, json.loads(response.data))
