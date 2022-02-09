# - *- coding: utf- 8 - *-
import sys
import xmltodict
import requests
import re

class WrongCountry(Exception):
    pass

class ServerError(Exception):
    pass

class UnexpectedError(Exception):
    pass

class Meteoalert(object):

    endpoint = "https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-{0}"

    def __init__(self, country, province, language='en-GB'):
        self.country = country.lower()
        self.province = province
        self.language = language

    def get_alert(self):
        """Retrieve alert data"""
        data = {}

        try:
            url = self.endpoint.format(self.country)
            response = requests.get(url, timeout=10)
        except Exception as err:
            raise(UnexpectedError(str(err)))

        self.check_status_code(response.status_code)

        # Why not simply use response.text instead of response._content + str/unicode?
        if sys.version_info[0] >= 3:
            text = str(response._content, 'utf-8')
        else:
            text = unicode(response._content, 'utf-8')

        # Parse the XML response for the alert feed and loop over the entries
        feed_data = xmltodict.parse(text)
        feed = feed_data.get('feed', [])
        entries = feed.get('entry', [])
        for entry in (entries if type(entries) is list else [entries]):
            #if entry.get('cap:areaDesc') != self.province:
            if re.search(rf"{self.province}", entry.get('cap:areaDesc'), re.IGNORECASE) == None:
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
                response = requests.get(cap_url, timeout=10)
            except Exception as err:
                raise(UnexpectedError(str(err)))

            self.check_status_code(response.status_code)

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


    def check_status_code(self, status_code):
        if status_code == 404:
            raise(WrongCountry('Apparently unsupported country name was specified'))
        elif status_code >= 500:
            raise(ServerError("Server error - status code: {0}".format(status_code)))
        elif status_code != 200:
            raise(UnexpectedError("Server returned unexpected status code: {0}".format(status_code)))
