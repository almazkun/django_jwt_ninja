# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestVies(TestCase):
    def setUp(self) -> None:
        self.user_data = {
            "username": "test",
            "email": "test@test.com",
            "password": "test",
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.user.set_password(self.user_data["password"])
        self.user.save()

    def test_token_obtain_pair(self):
        endpoint = reverse("api-1.0.0:token_obtain_pair")
        data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(endpoint, data, content_type="application/json")
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["username"], self.user_data["username"])
        self.assertTrue("access" in response_data)
        self.assertTrue("refresh" in response_data)

    def test_token_refresh(self):
        endpoint = reverse("api-1.0.0:token_obtain_pair")
        data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(endpoint, data, content_type="application/json")
        response_data = response.json()

        endpoint = reverse("api-1.0.0:token_refresh")
        data = {"refresh": response_data["refresh"]}
        response = self.client.post(endpoint, data, content_type="application/json")
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue("access" in response_data)
        self.assertTrue("refresh" in response_data)

    def test_token_verify(self):
        endpoint = reverse("api-1.0.0:token_obtain_pair")
        data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(endpoint, data, content_type="application/json")
        response_data = response.json()

        endpoint = reverse("api-1.0.0:token_verify")
        data = {"token": response_data["access"]}
        response = self.client.post(endpoint, data, content_type="application/json")
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response_data)

    def test_protected(self):
        endpoint = reverse("api-1.0.0:protected")
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, 401)

        endpoint = reverse("api-1.0.0:token_obtain_pair")
        data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(endpoint, data, content_type="application/json")
        response_data = response.json()

        endpoint = reverse("api-1.0.0:protected")
        response = self.client.get(
            endpoint, **{"HTTP_AUTHORIZATION": f"Bearer {response_data['access']}"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World!"})

        endpoint = reverse("api-1.0.0:protected")
        response = self.client.get(
            endpoint,
            **{
                "HTTP_AUTHORIZATION": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk1MjgzODAwLCJpYXQiOjE2OTUyODM1MDAsImp0aSI6IjAwNjQ3N2U5MWVjMjQwNWJhMGE5ZWFjNWJiYWE1OTViIiwidXNlcl9pZCI6MX0.254i8AE8NAWU9MeXPapbbdHDaUF_lxwfX4VBlanUnuI"
            },
        )
        response_data = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response_data,
            {
                "detail": "Given token not valid for any token type",
                "code": "token_not_valid",
                "messages": [
                    {
                        "token_class": "AccessToken",
                        "token_type": "access",
                        "message": "Token is invalid or expired",
                    }
                ],
            },
        )
