import unittest
from meteoalertapi import Meteoalert
coding=utf-8

meteo = Meteoalert("NL","Groningen","NL")
alert = meteo.get_alert()
for key, value in alert.items():
    print(key + ': ' + value)

meteo = Meteoalert("PT","LEIRIA","pt-PT")
alert = meteo.get_alert()
for key, value in alert.items():
    print(key + ': ' + value)

meteo = Meteoalert("PL","Białystok","en")
alert = meteo.get_alert()
for key, value in alert.items():
    print(key + ': ' + value)

class TesteMeteoalert(unittest.TestCase):

    def setUp(self):
        self.meteo = Meteoalert('IT', 'Toscana', 'it-IT')

    def test_get_alert(self):
        """Should return a dict (maybe empty)"""
        try:
            data = self.meteo.get_alert()
        except Exception:
            self.fail("'get_alert()' raised an unexpected exception!")
        self.assertEqual(type(data), dict)


if __name__ == '__main__':
    unittest.main()
