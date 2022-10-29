from django.test import TestCase
from accounts.models import User
from generic_functions.generic_test_helpers import random_string, random_length_string


class CreateUser:
    """
    Creates users in the database
    """

    def __init__(self, username=None, email=None, password=None, first_name=""):
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self._random_user()

    def _random_user(self):
        """
        If all fields are None, set a random user information
        """
        if not any([self.username, self.email, self.password]):
            self.username = random_length_string(low=4, high=16)
            self.email = f"{self.username}@example.com"
            self.password = random_length_string(low=8, high=16)

    def create_user(self):
        """
        Creates a user in to the database
        """
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email, 
            password=self.password,
            # first_name = random_length_string(low=4, high=16)
        )

    def create_or_set_admin(self):
        """
        Sets the user with admin privileges
        """
        try:
            self.user
        except AttributeError:
            self.create_user()

        self.user.is_staff = True
        self.user.save()


class UserTestCases(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_user_creation(self):
        """
        Checks that the User info matches, other than password.
        """
        u = CreateUser(username="Test", email="test@example.com", password="password123!")
        u.create_user()

        user = User.objects.get(username=u.username)

        self.assertEqual(user.username, "Test", "Username mis-match")
        self.assertEqual(user.email, "test@example.com", "Email mis-match")
        self.assertNotEqual(
            user.password,
            "password123!",
            "Password matched, PASSWORD STORED AS PLAIN TEXT!",
        )

    def test_get_saved_user_id_match(self):
        """
        Creates and returns User object. Then load User from DB, check that ID's match between the two.
        """
        u = CreateUser(username="Test", email="test@example.com", password="password123!")
        u.create_user()

        self.assertEqual(
            User.objects.get(username=u.username).id,
            1,
            "User ID mis-match",
        )
        self.assertEqual(
            User.objects.get(email=u.email).id,
            1,
            "User ID mis-match",
        )

    def test_admin_user(self):
        """
        Tests setting user as an admin user.
        """
        u = CreateUser(username="Test", email="test@example.com", password="password123!")
        u.create_or_set_admin()

        user = User.objects.get(username="Test")
        self.assertTrue(user.is_staff, "Admin flag not set.")
