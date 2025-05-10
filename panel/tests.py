from django.test import TestCase
from django.urls import reverse


class RoleBasedViewTests(TestCase):
    def test_panel_page(self):
        response = self.client.get(reverse('panel:panel'))
        self.assertRedirects(response, reverse('users:login'))