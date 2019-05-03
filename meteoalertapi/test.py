from meteoalertapi import Meteoalert

meteo = Meteoalert("IT","Toscana","it")
alert = meteo.get_alert()
#print(str(alert))
#print(alert['headline'])
for key, value in alert.items():
    print(key)
    print(value)
