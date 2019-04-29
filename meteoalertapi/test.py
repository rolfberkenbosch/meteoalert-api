from meteoalertapi import Meteoalert

meteo = Meteoalert("NL","Texel")
print(str(meteo.get_alert()))
