from starter_code.tests.unit.unit_base_test import UnitBaseTest
from starter_code.models.store import StoreModel


class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel('test')

        self.assertEqual(store.name, "test")
