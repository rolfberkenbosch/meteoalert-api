# - *- coding: utf- 8 - *-
import requests_mock
import unittest
import os
import re
import calendar
import time
try:
    from unittest import mock
except ImportError:
    import mock
from meteoalertapi import *

class TestMeteoalert(unittest.TestCase):

    def setUp(self):
        pass


    @requests_mock.mock()
    def test_get_alert(self, m):
        with open(self._file_path('uk_sample.xml')) as xml_file:
            m.register_uri('GET', '/feeds/meteoalarm-legacy-atom-united-kingdom', text=xml_file.read(), status_code=200)
        with open(self._file_path('uk_nothern_ireland_sample_detail.xml')) as xml_file:
            # get_alert() fetches every matching alert to rank them
            m.register_uri('GET', re.compile('/api/v1/warnings/feeds-united-kingdom/'),
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
            m.register_uri('GET', re.compile('/api/v1/warnings/feeds-ireland/'), text=xml_file.read(), status_code=200)

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
            m.register_uri('GET', re.compile('/api/v1/warnings/feeds-france/'),
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

    @requests_mock.mock()
    def test_most_severe_alert(self, m):
        self._register_multiple(m)
        self.meteo = Meteoalert('United-Kingdom', 'Highlands & Eilean Siar')

        """The feed lists yellow rain, amber wind, yellow wind; amber should win"""
        with mock.patch('time.time', return_value=self._timestamp('2026-10-24T12:00:00')):
            data = self.meteo.get_alert()
        self.assertEqual(data['event'], 'Amber wind warning')
        self.assertEqual(data['severity'], 'Severe')

    def test_expired_alert_not_preferred(self):
        meteo = Meteoalert('United-Kingdom', 'Highlands & Eilean Siar')
        expired_amber = {'event': 'Amber wind warning', 'severity': 'Severe',
                         'awareness_level': '3; Orange; Severe', 'expires': '2026-10-24T10:00:00+00:00'}
        current_yellow = {'event': 'Yellow rain warning', 'severity': 'Moderate',
                          'expires': '2026-10-25T15:00:00+00:00'}
        other_yellow = {'event': 'Yellow wind warning', 'severity': 'Moderate',
                        'expires': '2026-10-25T21:00:00+00:00'}

        with mock.patch('time.time', return_value=self._timestamp('2026-10-24T12:00:00')):
            ranked = max([expired_amber, current_yellow, other_yellow], key=meteo.alert_rank)
        """A current alert beats an expired, more severe one; ties keep feed order"""
        self.assertIs(ranked, current_yellow)

    def test_is_expired(self):
        now = self._timestamp('2026-10-24T12:00:00')
        with mock.patch('time.time', return_value=now):
            self.assertTrue(Meteoalert.is_expired('2026-10-24T11:59:59+00:00'))
            self.assertFalse(Meteoalert.is_expired('2026-10-24T12:30:00+00:00'))
            # 13:30 at +02:00 is 11:30 UTC
            self.assertTrue(Meteoalert.is_expired('2026-10-24T13:30:00+02:00'))
            self.assertFalse(Meteoalert.is_expired(None))

    def _register_multiple(self, m):
        with open(self._file_path('uk_multiple_sample.xml')) as xml_file:
            m.register_uri('GET', '/feeds/meteoalarm-legacy-atom-united-kingdom', text=xml_file.read(), status_code=200)
        for uuid, name in (('43e42eb0-196b-4fe7-b26e-1e3490954cc9', 'yellow_rain'),
                           ('ebbdecd5-fa00-40ec-9fa2-a4a5ea13b424', 'amber_wind'),
                           ('b0e83ff1-0a4b-4f2e-947a-c20b1432417c', 'yellow_wind')):
            with open(self._file_path('uk_multiple_detail_{}.xml'.format(name))) as xml_file:
                m.register_uri('GET', '/api/v1/warnings/feeds-united-kingdom/' + uuid,
                               text=xml_file.read(), status_code=200)

    @staticmethod
    def _timestamp(utc):
        return calendar.timegm(time.strptime(utc, '%Y-%m-%dT%H:%M:%S'))

    @staticmethod
    def _file_path(file_name):
        thispath = os.path.dirname(__file__)
        return "{}/{}".format(thispath, file_name)

if __name__ == '__main__':
    unittest.main()
