from downloader import List, Detail
import unittest
from unittest.mock import patch


class TestList(unittest.TestCase):
    def setUp(self):
        self.l1 = List(base_url='https://www.cars.com', path='/shopping/results/', page=5, page_size=20)
    
    def test_response_text(self):
        with patch('downloader.requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.text = "HTML content"
            list_page = self.l1.request_page()
            self.assertEqual(list_page, "HTML content")
    
    def test_parser(self):
        self.l1.text = '<a class="abcd" href="/abcd/3">'
        self.l1.parse_page(html_tag="a", css_class="abcd")
        detail_obj = Detail(base_url=self.l1.base_url, path="/abcd/3")
        self.assertEqual(detail_obj.path, self.l1.items[0].path)


class TestDetail(unittest.TestCase):
    def setUp(self):
        self.d1 = Detail(base_url='https://www.cars.com', path='/vehicledetail/e994d1fb-f242')

    def test_request(self):
        with patch('downloader.requests.get') as mocked_get:
            mocked_get.return_value.status_code = 200
            mocked_get.return_value.text = "HTML content"
            list_page = self.d1.request_page()
            mocked_get.assert_called_with('https://www.cars.com/vehicledetail/e994d1fb-f242', params={})
            self.assertEqual(list_page, "HTML content")



if __name__ == "__main__":
    unittest.main()
