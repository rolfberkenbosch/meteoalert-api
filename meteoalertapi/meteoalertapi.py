import sys
import xmltodict

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

class WrongCountry(Exception):
    pass

class NoProvince(Exception):
    pass

class Meteoalert(object):

    def __init__(self, country, province):
        # Constructer
        self.country = country
        self.province = province

    def get_alert(self):
        """ Retrieve alert """
        id = ""
        d = {}
        country=self.country.upper()
        province=self.province

        try:
            file = urlopen('http://meteoalarm.eu/ATOM/'+ country +'.xml')
            data = file.read()
            file.close()
        except:
            raise(WrongCountry())

        data = xmltodict.parse(data)

        if "entry" in data['feed']:
            for i in data['feed']['entry']:
                if i['cap:areaDesc'] == province:
                    if id == "":
                        for x in i['link']:
                            if('cap.xml' in x['@href']):
                                try:
                                    file = urlopen(x['@href'])
                                    data2 = file.read()
                                    file.close()
                                except:
                                    raise(WrongCountry())
                                data2 = xmltodict.parse(data2)

                                if "info" in data2['alert']:
                                    for i in data2['alert']['info']:
                                        if i['language'] == 'en-GB':
                                            for x in i:
                                                if(x != 'area'):
                                                    if(x == 'parameter'):
                                                        pass
                                                        for z in i[x]:
                                                            d[z['valueName']]=z['value']
                                                    else:
                                                        d[x]=i[x]
            return d
