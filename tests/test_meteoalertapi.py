# - *- coding: utf- 8 - *-
import requests_mock
import unittest
from meteoalertapi import *

class TestMeteoalert(unittest.TestCase):

    def setUp(self):
        pass


    def test_get_alert(self):
        self.meteo = Meteoalert('netherlands', 'Groningen', 'ne-NL')

        """Should return a dict (maybe empty)"""
        try:
            data = self.meteo.get_alert()
        except Exception:
            self.fail("'get_alert()' raised an unexpected exception!")
        self.assertEqual(type(data), dict)


    def test_wrong_country_name(self):
        self.meteo = Meteoalert('wrong_country_name', 'some_city', 'some-lang')

        """Should throw WrongCountry exception"""
        self.assertRaises(WrongCountry, self.meteo.get_alert)


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


if __name__ == '__main__':
    unittest.main()
