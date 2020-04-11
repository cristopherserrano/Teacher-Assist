from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_frmaework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserTest(TestCase):
    def setup(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        payload = {
            'email': 'test@gmail.com',
            'user': 'Teacher teach',
            'password': 'Password1234!'
        }
        request = self.client.post(CREATE_USER_URL, payload)
        self.assetEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get()

    def test_create_invalid_user_failure(self):
        # create with an empty string
        # create with already created username
        # create with no email standards

    def test_create_valid_password_success(self):
        # password standards
        # empty string


class PrivateUserTest(TestCase):
