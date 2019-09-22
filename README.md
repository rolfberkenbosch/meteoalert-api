# meteoalarm-api


![PyPI](https://img.shields.io/pypi/v/meteoalertapi.svg?style=for-the-badge|https://pypi.org/project/meteoalertapi)
![Travis (.org)](https://img.shields.io/travis/rolfberkenbosch/meteoalert-api.svg?style=for-the-badge)

(Unofficial) Python wrapper for the MeteoAlarm.eu website (European Weahter alarm), which can be used to look if your province in your country has currently had a weather alarm.

## Installation

Using Pip:

```console
pip install meteoalertapi
```

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
