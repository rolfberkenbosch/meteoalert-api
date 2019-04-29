# meteoalarm-api
(Unofficial) Python wrapper for the MeteoAlarm.eu website (European Weahter alarm), which can be used to look if your province in your country has currently had a weather alarm.


## Code Example
```python
from meteoalertapi import Meteoalert

# Find you country and province on http://meteoalarm.eu/
meteo = Meteoalert('country_letters', 'province_name')

# Get the weather alarm from your place
meteo = Meteoalert('country_letters', 'province_name')
print(str(meteo.get_alert()))
```

## Changelog
See the [CHANGELOG](./CHANGELOG.md) file.

## License
MIT