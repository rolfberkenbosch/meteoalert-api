# - *- coding: utf- 8 - *-
import sys
import xmltodict
import requests


class WrongCountry(Exception):
    pass


class Meteoalert(object):

    def __init__(self, country, province, language='en-GB'):
        self.country = country.lower()
        self.province = province
        self.language = language

    def get_alert(self):
        """Retrieve alert data"""
        data = {}

        try:
            url = "https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-{0}".format(self.country)
            response = requests.get(url)
        except Exception:
            raise(WrongCountry())

        # Parse the XML response for the alert feed and loop over the entries
        if sys.version_info[0] >= 3:
            text = str(response._content, 'utf-8')
        else:
            text = unicode(response._content, "utf-8")

        feed_data = xmltodict.parse(text)
        feed = feed_data.get('feed', [])
        entries = feed.get('entry', [])
        for entry in (entries if type(entries) is list else [entries]):
            if entry.get('cap:areaDesc') != self.province:
                continue

            # Get the cap URL for additional alert data
            cap_url = None
            for link in entry.get('link'):
                if 'hub' in link.get('@href'):
                    cap_url = link.get('@href')

            print(cap_url)

            if not cap_url:
                continue

            # Parse the XML response for the alert information
            try:
                response = requests.get(cap_url)
            except Exception:
                raise(WrongCountry())

            if sys.version_info[0] >= 3:
                text = str(response._content, 'utf-8')
            else:
                text = unicode(response._content, "utf-8")

            alert_data = xmltodict.parse(text)
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
            try:
                parameters  = translation.get('parameter', [])
                for parameter in parameters:
                    data[parameter.get('valueName')] = parameter.get('value')
            except:
                pass
                pass
            break
        return data
