from django.test import TestCase
from django.urls import reverse

class RangoViewsTests(TestCase):
    def test_index_page_loads(self):
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rango says")

    def test_about_page_loads(self):
        response = self.client.get(reverse('rango:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "about page.")
