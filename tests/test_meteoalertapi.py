# - *- coding: utf- 8 - *-
import unittest
from meteoalertapi import Meteoalert


class TestMeteoalert(unittest.TestCase):

    def setUp(self):
        self.meteo = Meteoalert('netherlands', 'Groningen', 'ne-NL')

    def test_get_alert(self):
        """Should return a dict (maybe empty)"""
        try:
            data = self.meteo.get_alert()
        except Exception:
            self.fail("'get_alert()' raised an unexpected exception!")
        self.assertEqual(type(data), dict)
