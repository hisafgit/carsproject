from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cars.models import Car, Brand, ExteriorColor, Transmission
from django.forms.models import model_to_dict


class TestCarFilterList(APITestCase):
    @classmethod
    def setUp(self):
        self.brand1 = Brand.objects.create(name="Brand111")
        self.brand2 = Brand.objects.create(name="Brand222")
        self.extcol1 = ExteriorColor.objects.create(color="ExteriorColor111")
        self.extcol2 = ExteriorColor.objects.create(color="ExteriorColor222")
        self.trans1 = Transmission.objects.create(transmission_type="TransmissionColor111")
        self.trans2 = Transmission.objects.create(transmission_type="TransmissionColor222")
        self.car1 = Car.objects.create(title="Title111", price=111, \
            img_url="https://image111.com", brand=self.brand1, year=111, \
                extcolor=self.extcol1, trans=self.trans1)
        self.base_url = '/cars/list/'


    def test_response_code(self):
        response = self.client.get(self.base_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_year_filter(self):
        response = self.client.get(self.base_url, QUERY_STRING="year=111")
        self.assertEqual(dict(response.data["results"][0])['year'], 111)

    def test_brand_filter(self):
        response = self.client.get(self.base_url, QUERY_STRING="brand=Brand111")
        self.assertEqual(dict(response.data["results"][0])['brand'], "Brand111")
    
    def test_multiple_filters(self):
        response = self.client.get(self.base_url, QUERY_STRING="brand=Brand111&extcolor=ExteriorColor111")
        self.assertEqual(dict(response.data["results"][0])['brand'], "Brand111")
        self.assertEqual(dict(response.data["results"][0])['extcolor'], "ExteriorColor111")


    