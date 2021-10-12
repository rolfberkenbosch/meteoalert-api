# meteoalarm-api


![PyPI](https://img.shields.io/pypi/v/meteoalertapi.svg?style=for-the-badge|https://pypi.org/project/meteoalertapi)
![Travis (.org)](https://img.shields.io/travis/rolfberkenbosch/meteoalert-api.svg?style=for-the-badge)

An unofficial Python wrapper for [MeteoAlarm.org](https://meteoalarm.org) website (European Weather alerts), which can be used to check if a given province in your country has currently a weather alert.

## Installation

Using Pip:

```console
pip install meteoalertapi
```

## Code Example

```python
from meteoalertapi import Meteoalert

# Find you country and province on https://meteoalarm.org/ or https://feeds.meteoalarm.org/
meteo = Meteoalert('country', 'province_name')

# Get the weather alarm for your place
meteo = Meteoalert('country', 'province_name')
print(str(meteo.get_alert()))
```

## Changelog

See the [CHANGELOG](./CHANGELOG.md) file.

## License

MIT
