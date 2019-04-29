import sys
import urllib2
import xmltodict

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
            file = urllib2.urlopen.urlopen('http://meteoalarm.eu/ATOM/'+ country +'.xml')
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
                                    file = urllib2.urlopen.urlopen(x['@href'])
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
