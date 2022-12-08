# - *- coding: utf- 8 - *-
import requests_mock
import unittest
import os
from meteoalertapi import *

class TestMeteoalert(unittest.TestCase):

    def setUp(self):
        pass


    @requests_mock.mock()
    def test_get_alert(self, m):
        with open(self._file_path('uk_sample.xml')) as xml_file:
            m.register_uri('GET', '/feeds/meteoalarm-legacy-atom-united-kingdom', text=xml_file.read(), status_code=200)
        with open(self._file_path('uk_nothern_ireland_sample_detail.xml')) as xml_file:
            m.register_uri('GET', '/api/v1/warnings/feeds-united-kingdom/a4647d38-40ea-4c01-b874-4e2b3df383b9',
                           text=xml_file.read(), status_code=200)

        self.meteo = Meteoalert('United-Kingdom', 'Northern Ireland')

        """Should return a dict (maybe empty)"""
        try:
            data = self.meteo.get_alert()
        except Exception:
            self.fail("'get_alert()' raised an unexpected exception!")
        self.assertEqual(type(data), dict)
        self.assertGreater(len(data), 0)


    def test_wrong_country_name(self):
        self.meteo = Meteoalert('wrong_country_name', 'some_city', 'some-lang')

        """Should throw WrongCountry exception"""
        self.assertRaises(WrongCountry, self.meteo.get_alert)

    @requests_mock.mock()
    def test_retrieve_alert_by_code(self, m):
        with open(self._file_path('ireland_sample.xml')) as xml_file:
            m.register_uri('GET', '/feeds/meteoalarm-legacy-atom-ireland', text=xml_file.read(), status_code=200)
        with open(self._file_path('ireland_sample_detail.xml')) as xml_file:
            m.register_uri('GET', '/api/v1/warnings/feeds-ireland/558830a2-74a1-402a-915c-ab365ec68d25', text=xml_file.read(), status_code=200)

        self.meteo = Meteoalert('Ireland', 'EI25')
        data = self.meteo.get_alert()
        self.assertEqual(type(data), dict)
        self.assertGreater(len(data), 0)

        self.meteo = Meteoalert('Ireland', 'FAKE')
        data = self.meteo.get_alert()
        self.assertEqual(type(data), dict)
        self.assertEqual(len(data), 0)

    @requests_mock.mock()
    def test_lookup_by_code_and_area_name(self, m):
        with open(self._file_path('france_sample.xml')) as xml_file:
            m.register_uri('GET', '/feeds/meteoalarm-legacy-atom-france', text=xml_file.read(), status_code=200)
        with open(self._file_path('france_sample_detail.xml')) as xml_file:
            m.register_uri('GET', '/api/v1/warnings/feeds-france/04d497d4-d114-4d6b-93ba-13fa7ed577fe',
                           text=xml_file.read(), status_code=200)

        self.meteo = Meteoalert('France', 'Haute Savoie')
        data = self.meteo.get_alert()
        self.assertEqual(type(data), dict)
        self.assertGreater(len(data), 0)

        # ensure we can get the French localised version
        self.meteo = Meteoalert('France', 'Haute Savoie', 'fr-FR')
        data = self.meteo.get_alert()
        self.assertEqual(type(data), dict)
        self.assertGreater(len(data), 0)

        # ensure we can get the alert by area code
        self.meteo = Meteoalert('France', 'FR822', 'fr-FR')
        data = self.meteo.get_alert()
        self.assertEqual(type(data), dict)
        self.assertGreater(len(data), 0)

        self.meteo = Meteoalert('France', 'FAKE')
        data = self.meteo.get_alert()
        self.assertEqual(type(data), dict)
        self.assertEqual(len(data), 0)

    def test_server_not_reachable(self):
        self.meteo = Meteoalert('poland', 'krakow', 'en-US')
        self.meteo.endpoint = "https://simulate-dns-problem-with-meteo.zzzzzz/{0}"

        """Should throw UnexpectedError exception"""
        self.assertRaises(UnexpectedError, self.meteo.get_alert)


    def test_server_error(self):
        with requests_mock.mock() as m:
            m.get(requests_mock.ANY, status_code=500, text='simulated server error')            
            self.meteo = Meteoalert('wrong_country_name', 'some_city', 'some-lang')

            """Should throw ServerError exception"""
            self.assertRaises(ServerError, self.meteo.get_alert)

    @staticmethod
    def _file_path(file_name):
        thispath = os.path.dirname(__file__)
        return "{}/{}".format(thispath, file_name)

if __name__ == '__main__':
    unittest.main()
