from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('user test', '123456')

        self.assertEqual(user.username, 'user test',
                         "The username of the user after creation does not equal the constructor argument")
        self.assertEqual(user.password, '123456',
                         "The password of the user after creation does not equal the constructor argument")
