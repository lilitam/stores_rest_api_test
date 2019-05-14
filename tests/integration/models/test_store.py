from starter_code.models.item import ItemModel
from starter_code.models.store import StoreModel
from starter_code.tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test')

        self.assertListEqual(store.items.all(), [])

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'))
            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name('test'))
            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name('test'))

    def test_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item')

    def test_store_json(self):
        with self.app_context():
            store = StoreModel('test')
            store.save_to_db()
            expected = {
                'name': 'test',
                'items': []
            }
            self.assertDictEqual(store.json(), expected)
            item = ItemModel('test_item', 19, 1)
            item.save_to_db()
            expected_with_items = {
                'name': 'test',
                'items': [{'name': 'test_item', 'price': 19}]
            }
            self.assertDictEqual(store.json(), expected_with_items)

