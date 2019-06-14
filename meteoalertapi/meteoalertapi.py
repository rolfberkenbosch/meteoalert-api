import sys
import xmltodict
import requests


class WrongCountry(Exception):
    pass


class Meteoalert(object):

    def __init__(self, country, province, language='en-GB'):
        self.country = country.upper()
        self.province = province
        self.language = language

    def get_alert(self):
        """Retrieve alert data"""
        data = {}

        try:
            url = "http://meteoalarm.eu/ATOM/{0}.xml".format(self.country)
            response = requests.get(url)
        except Exception:
            raise(WrongCountry())

        # Parse the XML response for the alert feed and loop over the entries
        feed_data = xmltodict.parse(str(response._content, 'utf-8'))
        feed = feed_data.get('feed', [])
        for entry in feed.get('entry', []):
            if entry.get('cap:areaDesc') != self.province:
                continue

            # Get the cap URL for additional alert data
            cap_url = None
            for link in entry.get('link'):
                if 'cap.xml' in link.get('@href'):
                    cap_url = link.get('@href')

            if not cap_url:
                continue

            # Parse the XML response for the alert information
            try:
                response = requests.get(cap_url)
            except Exception:
                raise(WrongCountry())
            alert_data = xmltodict.parse(str(response._content, 'utf-8'))
            alert = alert_data.get('alert', {})
            # Get the alert data in the requested language
            translations = alert.get('info', [])

            try:
                for translation in translations:
                    if self.language not in translation.get('language'):
                        continue

                    # Store alert information in the data dict
                    for key, value in translation.items():
                        # Check if the value is a string
                        # Python 2 uses 'basestring' while Python 3 requires 'str'
                        if isinstance(value, str if sys.version_info[0] >= 3 else basestring):
                            data[key] = value

                    # Don't check other languages
                    break
            except:
                for key, value in translations.items():
                    if isinstance(value, str if sys.version_info[0] >= 3 else basestring):
                        data[key] = value

            break
        return data
