from meteoalertapi import Meteoalert

meteo = Meteoalert("IT", "Toscana", language="it")
alert = meteo.get_alert()
for key, value in alert.items():
    print(key + ': ' + value)
