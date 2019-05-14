from starter_code.models.item import ItemModel
from starter_code.models.store import StoreModel
from starter_code.tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual({'name': 'test', 'items': []}, json.loads(response.data))
                self.assertIsNotNone(StoreModel.find_by_name('test'))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.post('/store/test')
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "A store with name 'test' already exists."}, json.loads(response.data))

    def test_delete_Store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.delete('/store/test')

                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))
                self.assertIsNone(StoreModel.find_by_name('test'))
                self.assertEqual(response.status_code, 200)

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.get('/store/test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'test', 'items': []}, json.loads(response.data))



    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/test')

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                ItemModel('test_item', 19, 1).save_to_db()
                response = client.get('/store/test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'test', 'items': [{'name': 'test_item', 'price': 19}]}, json.loads(response.data))


    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'name': 'test', 'items': []}]}, json.loads(response.data))

    def test_store_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                ItemModel('test_item', 19, 1).save_to_db()
                response = client.get('/stores')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'name': 'test', 'items': [{'name': 'test_item', 'price': 19}]}]}, json.loads(response.data))
