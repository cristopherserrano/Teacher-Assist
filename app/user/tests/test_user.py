from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:authToken')
SELF_URL = reverse('user:self')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'Password1234!',
            'name': 'name',
        }
        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(
            user.check_password(data['password'])
        )
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        data = {'email': 'test@londonappdev.com', 'password': 'testpass',
                'name': 'name'}
        create_user(**data)
        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        data = {'email': 'test@gmail.com',
                'password': 'pas', 'name': 'techer'}
        res = self.client.post(CREATE_USER_URL, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=data['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token(self):
        data = {'email': 'test@gmail.com',
                'password': 'password1234!', 'name': 'teacher teach'}
        create_user(**data)
        res = self.client.post(TOKEN_URL, data)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_creds(self):
        create_user(email='test@gmail.com', password="testpass")
        data = {'email': 'test@gmail.com', 'password': 'error'}
        res = self.client.post(TOKEN_URL, data)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        data = {'email': 'test@gmail.com', 'password': 'jknkjnknk'}
        res = self.client.post(TOKEN_URL, data)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        res = self.client.post(
            TOKEN_URL, {'email': 'email', 'password': '', 'name': 'teach'})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        res = self.client.get(SELF_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserTests(TestCase):

    def setUp(self):
        self.user = create_user(
            email='test@gmail.com',
            password='passwrod1234',
            name='test'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        res = self.client.get(SELF_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        res = self.client.post(SELF_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        data = {'name': 'test test', 'password': 'sdaksndkasdnaskdnsa'}

        res = self.client.patch(SELF_URL, data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, data['name'])
        self.assertTrue(self.user.check_password(data['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

# to do:
    # def test_create_invalid_user_failure(self):
    #     # create with an empty string
    #     # create with already created username
    #     # create with no email standards

    # def test_create_valid_password_success(self):
    #     # password standards
    #     # empty string
