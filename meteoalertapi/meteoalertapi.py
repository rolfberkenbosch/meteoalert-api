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

    def _fetch_alerts(self, limit=None):
        """Retrieve alert or alerts data, stopping after `limit` alerts"""
        alerts = []

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
            if not self.is_location_match(entry, self.province):
                continue

            # Get the cap URL for additional alert data
            cap_url = None
            for link in entry.get('link'):
                if 'application/cap+xml' == link.get('@type'):
                    cap_url = link.get('@href')

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

            data = {}
            translation = None
            if isinstance(translations, dict):
                # A single <info> block is used whatever its language
                translation = translations
            else:
                for candidate in translations:
                    if self.language in (candidate.get('language') or ''):
                        translation = candidate
                        break

            if translation is None:
                continue

            # Store alert information in the data dict
            for key, value in translation.items():
                # Check if the value is a string
                # Python 2 uses 'basestring' while Python 3 requires 'str'
                if isinstance(value, str if sys.version_info[0] >= 3 else basestring):
                    data[key] = value

            parameters = translation.get('parameter', [])
            if isinstance(parameters, dict):
                parameters = [parameters]
            for parameter in parameters:
                data[parameter.get('valueName')] = parameter.get('value')

            # CAP message metadata, to track alerts and handle Update/Cancel
            data['message_type'] = entry.get('cap:message_type')
            data['identifier'] = entry.get('cap:identifier')
            data['references'] = alert.get('references')
            data['sent'] = alert.get('sent')

            alerts.append(data)
            if limit is not None and len(alerts) >= limit:
                break

        return alerts

    def get_alert(self):
        """Retrieve the first alert."""
        alerts = self._fetch_alerts(limit=1)
        return alerts[0] if alerts else {}

    def get_alerts(self):
        """Retrieve all alerts, most severe first."""
        alerts = self._fetch_alerts()
        # Stable sort: alerts with the same level keep the feed order
        return sorted(alerts, key=self._awareness_level, reverse=True)

    @staticmethod
    def _awareness_level(alert):
        """Leading number of e.g. '3; orange; Severe', or 0 if missing"""
        try:
            return int(alert.get('awareness_level', '').split(';')[0])
        except ValueError:
            return 0

    def is_location_match(self, entry, province):
        # Attempt to match the province first by regex on name
        if re.search(rf"{self.province}", entry.get('cap:areaDesc'), re.IGNORECASE):
            return True

        # then by areaCode
        elif entry.get('cap:geocode') and entry.get('cap:geocode')['value']:
            if entry.get('cap:geocode')['value'] == province:
                return True

        return False


    def check_status_code(self, status_code):
        if status_code == 404:
            raise(WrongCountry('Apparently unsupported country name was specified'))
        elif status_code >= 500:
            raise(ServerError("Server error - status code: {0}".format(status_code)))
        elif status_code != 200:
            raise(UnexpectedError("Server returned unexpected status code: {0}".format(status_code)))
