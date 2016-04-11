from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from simple_app.utils import ReliableUrlValidator


class DomainPostViewTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super(DomainPostViewTests, cls).setUpClass()
        cls.patch = patch.object(ReliableUrlValidator, 'available_on_the_internet', return_value=True)
        cls.patch.start()

    @classmethod
    def tearDownClass(cls):
        super(DomainPostViewTests, cls).tearDownClass()
        cls.patch.stop()

    def setUp(self):
        self.url = reverse("domains")
        self.obj_data = {"name": "https://test.com", "is_private": False}
        self.client.force_authenticate(User(), 'fake_token')

    def test_create_domain_passes(self):
        response = self.client.post(self.url, data=self.obj_data, format='json')
        self.assertContains(response, text=self.obj_data['name'], status_code=201)

    def test_create_private_domain_passes(self):
        self.obj_data['is_private'] = True
        response = self.client.post(self.url, data=self.obj_data, format='json')
        self.assertContains(response, text=self.obj_data['name'], status_code=201)

    def test_create_domain_without_name_fails(self):
        self.obj_data.pop('name')
        response = self.client.post(self.url, data=self.obj_data, format='json')
        self.assertContains(response, text='name', status_code=400)

    @patch.object(ReliableUrlValidator, 'available_on_the_internet', return_value=False)
    def test_create_unresponsive_domain_fails(self, mocked_validator):
        response = self.client.post(self.url, data=self.obj_data, format='json')
        self.assertContains(response, text="The response from domain", status_code=400)

    def test_create_domain_with_invalid_name_fails(self):
        self.obj_data['name'] = 'dummy/domain'
        response = self.client.post(self.url, data=self.obj_data, format='json')
        self.assertContains(response, text='name', status_code=400)

    def test_create_domain_only_with_name_passes(self):
        self.obj_data.pop('is_private')
        response = self.client.post(self.url, data=self.obj_data, format='json')
        self.assertContains(response, text=self.obj_data['name'], status_code=201)

    def test_create_domain_only_with_name_defines_default_private_flag(self):
        self.obj_data.pop('is_private')
        response = self.client.post(self.url, data=self.obj_data, format='json')
        self.assertIsNotNone(response.data['is_private'])

    def test_create_domain_with_excessive_fields_passes(self):
        self.obj_data['dummy'] = 'test'
        response = self.client.post(self.url, data=self.obj_data, format='json')
        self.assertContains(response, text=self.obj_data['name'], status_code=201)

    def test_create_domain_by_anonymous_fails(self):
        self.client.logout()
        response = self.client.post(self.url, data=self.obj_data, format='json')
        self.assertContains(response, text='Authentication credentials were not provided.', status_code=403)


class DomainGetViewTests(APITestCase):

    def setUp(self):
        self.client.force_authenticate(User(), 'fake_token')
        with patch.object(ReliableUrlValidator, 'available_on_the_internet', return_value=True):
            self.pub_domain = self.client.post(
                path=reverse("domains"), format='json',
                data={"name": "https://test1.com", "is_private": False}
            ).data
            self.prt_domain = self.client.post(
                path=reverse("domains"), format='json',
                data={"name": "https://test2.com", "is_private": True}
            ).data

        self.pub_url = reverse("domain", kwargs={'pk': self.pub_domain['id']})
        self.prt_url = reverse("domain", kwargs={'pk': self.prt_domain['id']})

    def test_get_domain_passes(self):
        response = self.client.get(self.pub_url)
        self.assertContains(response, text=self.pub_domain['name'], status_code=200)

    def test_get_private_domain_passes(self):
        response = self.client.get(self.prt_url)
        self.assertContains(response, text=self.prt_domain['name'], status_code=200)

    def test_get_not_existing_domain_fails(self):
        url = reverse('domain', kwargs={'pk': 55555})
        response = self.client.get(url)
        self.assertContains(response, text='Not found', status_code=404)

    def test_get_private_domain_by_anonymous_fails(self):
        self.client.logout()
        response = self.client.get(self.prt_url)
        self.assertContains(response, text='Authentication credentials were not provided.', status_code=403)

    def test_get_public_domain_by_anonymous_passes(self):
        self.client.logout()
        response = self.client.get(self.pub_url)
        self.assertContains(response, text=self.pub_domain['name'], status_code=200)


class DomainListViewTests(APITestCase):

    def setUp(self):
        self.client.force_authenticate(User(), 'fake_token')
        self.url = reverse("domains")
        with patch.object(ReliableUrlValidator, 'available_on_the_internet', return_value=True):
            self.pub_domain = self.client.post(
                path=self.url, format='json',
                data={"name": "https://test1.com", "is_private": False}
            ).data
            self.prt_domain = self.client.post(
                path=self.url, format='json',
                data={"name": "https://test2.com", "is_private": True}
            ).data

    def test_list_domains_returns_expected_results(self):
        response = self.client.get(self.url)
        self.assertContains(response, text='', status_code=200)
        self.assertTrue(isinstance(response.data, list), 'Received not a list in response')
        self.assertGreater(len(response.data), 1)

    def test_list_domains_hides_private_domains_for_anonymous(self):
        with patch.object(ReliableUrlValidator, 'available_on_the_internet', return_value=True):
            self.client.post(path=self.url, format='json',
                             data={"name": "https://test3.com", "is_private": False})
        self.client.logout()
        response = self.client.get(self.url)
        self.assertContains(response, text='', status_code=200)
        no_privates = not any(domain for domain in response.data if domain['is_private'])
        self.assertTrue(no_privates, 'Received private domain in response')
        self.assertGreater(len(response.data), 1)
