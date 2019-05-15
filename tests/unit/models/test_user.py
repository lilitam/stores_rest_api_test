from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest

class UnitTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel("username", "ppp")

        self.assertEqual(user.username, "username")
        self.assertEqual(user.password, "ppp", "The password is not the same as it defined in constructor")