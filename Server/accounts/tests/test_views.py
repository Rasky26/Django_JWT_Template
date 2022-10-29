from django.test import Client, TestCase
from accounts.tests.test_models import CreateUser


class CreateCustomerViews(CreateUser):
    """
    Container for generic user access and information
    """

    def __init__(self, username=None, email=None, password=None):
        CreateUser.__init__(self, username, email, password)
        self.client = Client()
        self.access_token = None
        self.refresh_token = None

    def login(self):
        """
        Logs in the current user
        """
        try:
            self.user
        except AttributeError:
            self.create_user()

        self.login_response = self.client.post(
            path="/accounts/token/",
            data=dict(email=self.email, password=self.password),
        )

        # If login was valid, set additional fields
        if self.login_response.status_code == 200:
            # Update with the return tokens (both access and refresh)
            self.access_token = self.login_response.data["access"]
            self.refresh_token = self.login_response.data["refresh"]
            # Update the self.client with JWT token header
            self.client = Client(AUTHORIZATION=f"JWT {self.access_token}")

    def logout(self):
        """
        Logs the current user out
        """
        self.logout_response = self.client.post(
            path="/accounts/logout/blacklist/",
            data=dict(refresh_token=self.refresh_token)
        )


class UserViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def setUp(self) -> None:
        return super().setUp()

    def test_user_log_in(self):
        """
        Test the user logins in and gets a 64-character token
        """
        u = CreateCustomerViews()
        u.login()

        self.assertEqual(
            u.login_response.status_code,
            200,
            f"Login status_code not 200. Got {u.login_response.status_code} instead.",
        )
        self.assertRegex(
            u.login_response.data["access"],
            "^[\w-]*\.[\w-]*\.[\w-]*$",
            f"Unexpected JWT access token. Got {u.login_response.data['access']}",
        )
        self.assertRegex(
            u.login_response.data["refresh"],
            "^[\w-]*\.[\w-]*\.[\w-]*$",
            f"Unexpected JWT refresh token. Got {u.login_response.data['refresh']}",
        )
        self.assertRegex(
            u.access_token,
            "^[\w-]*\.[\w-]*\.[\w-]*$",
            f"Unexpected JWT access token. Got {u.access_token}",
        )
        self.assertRegex(
            u.refresh_token,
            "^[\w-]*\.[\w-]*\.[\w-]*$",
            f"Unexpected JWT refresh token. Got {u.refresh_token}",
        )

    def test_user_logout(self):
        """
        Tests the user can logout with a token.
        """
        u = CreateCustomerViews()

        # Check for successful login
        u.login()

        self.assertEqual(
            u.login_response.status_code,
            200,
            f"Login status_code not 200. Got {u.login_response.status_code} instead.",
        )
        self.assertRegex(
            u.login_response.data["access"],
            "^[\w-]*\.[\w-]*\.[\w-]*$",
            f"Unexpected JWT access token. Got {u.login_response.data['access']}",
        )
        self.assertRegex(
            u.login_response.data["refresh"],
            "^[\w-]*\.[\w-]*\.[\w-]*$",
            f"Unexpected JWT refresh token. Got {u.login_response.data['refresh']}",
        )
        self.assertRegex(
            u.access_token,
            "^[\w-]*\.[\w-]*\.[\w-]*$",
            f"Unexpected JWT access token. Got {u.access_token}",
        )
        self.assertRegex(
            u.refresh_token,
            "^[\w-]*\.[\w-]*\.[\w-]*$",
            f"Unexpected JWT refresh token. Got {u.refresh_token}",
        )


        # Check for successful logout
        u.logout()

        self.assertEqual(
            u.logout_response.status_code,
            205,
            f"Logout status code not 205. Got {u.logout_response.status_code} instead.",
        )
        self.assertIsNone(
            u.logout_response.data, "Received data when it should have been None"
        )

    def test_user_log_in_bad_email(self):
        """
        Failed login when invalid email is passed with valid password
        """
        u = CreateCustomerViews()
        # Create an account with email and password
        u.create_user()
        # Set a different email
        u.email = "bad_email"
        # Attempt login using invalid email and valid password
        u.login()

        self.assertEqual(
            u.login_response.status_code,
            401,
            f"Login status_code not 401. Got {u.login_response.status_code} instead.",
        )
        self.assertEqual(
            u.login_response.data["detail"].title(),
            "No Active Account Found With The Given Credentials",
            "Login error message does not match",
        )
        self.assertEqual(
            u.login_response.data["detail"].code,
            "no_active_account",
            "Login error code does not match",
        )

    def test_user_log_in_bad_password(self):
        """
        Failed login when bad password is supplied
        """
        u = CreateCustomerViews()
        # Create an account with email and password
        u.create_user()
        # Set a different password (not reset_password, just send a bad password via POST)
        u.password = "bad_password"
        # Attempt login using valid email and invalid password
        u.login()

        self.assertEqual(
            u.login_response.status_code,
            401,
            f"Login status_code not 401. Got {u.login_response.status_code} instead.",
        )
        self.assertEqual(
            u.login_response.data["detail"].title(),
            "No Active Account Found With The Given Credentials",
            "Login error message does not match",
        )
        self.assertEqual(
            u.login_response.data["detail"].code,
            "no_active_account",
            "Login error code does not match",
        )

    def test_create_standard_user_then_grant_admin_status(self):
        """
        Create a standard user and then grant admin status
        """
        u = CreateCustomerViews()
        u.login()

        self.assertFalse(u.user.is_staff, "User was already assigned as admin")
        u.user.is_staff = True
        self.assertTrue(u.user.is_staff, "User was not set as staff")

    def test_create_admin_user_then_remove_admin_status(self):
        """
        Create an admin user and then remove admin status
        """
        u = CreateCustomerViews()
        u.create_or_set_admin()
        u.login()

        self.assertTrue(u.user.is_staff, "User was not set as staff")
        u.user.is_staff = False
        self.assertFalse(u.user.is_staff, "User was already assigned as admin")
