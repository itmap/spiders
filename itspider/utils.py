#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import hashlib
import logging
import re
import jieba
from scrapy.utils.project import get_project_settings
from geopy.geocoders import Baidu
from geopy.distance import vincenty


settings = get_project_settings()
ak = settings.get("MAP_AK")
baidu_url = "http://api.map.baidu.com/geocoder/v2/?address=%s&city=%s&output=json&ak=%s"
no_city_baidu_url = "http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=%s"
reverse_url = "http://api.map.baidu.com/geocoder/v2/?ak=%s&location=%s,%s&output=json&pois=1"
location_reverse_url = "http://api.map.baidu.com/geocoder/v2/?ak=%s&%s&output=json&pois=1"

logger = logging.getLogger("exception")

geo = Baidu(ak)

def md5(md):
    s = md.encode('utf-8')
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def get_geo_search_retry(address, city=None):
    for i in range(5):
        try:
            info = geo.search(address, city=city, ret_coordtype='gcj02ll',
                              city_limit=True, timeout=5)
            if info: return info
        except Exception as e:
            logger.exception(u'geo search error ====> {}:{}'.format(address.encode('utf-8'), city.encode('utf-8')))
            logger.exception(e)
    else:
        return None

def get_geo_code_retry(address, city=None):
    for i in range(5):
        try:
            info = geo.geocode(address, city=city, ret_coordtype='gcj02ll',
                               timeout=5)
            if info: return info
        except Exception as e:
            logger.exception(u'geo search error ====> {}:{}'.format(address.encode('utf-8'), city.encode('utf-8')))
            logger.exception(e)
    else:
        return None

def get_geo_info(name, place, city=None):
    info = get_geo_search_retry(name, city=city) if name else None
    if not info:
        info = get_geo_code_retry(name, city=city)
    data = get_geo_search_retry(place, city=city) if place else None
    if not data:
        data = get_geo_code_retry(place, city=city)
    if not info and not data:
        return False
    if not info:
        r_info = geo.reverse((data.latitude, data.longitude), coordtype="gcj02ll", timeout=5)
        return data
    if not data:
        r_data = geo.reverse((info.latitude, info.longitude), coordtype="gcj02ll", timeout=5)
        return info
    dis = vincenty((info.latitude, info.longitude), (data.latitude,
                                                    data.longitude)).m
    return info if dis < 800 else data

def get_geo_location(place, city=None):
    search = get_geo_search_retry(place, city=city)
    geocode = get_geo_code_retry(place, city=city)
    if not search and not geocode:
        return False
    if not search: return geocode.raw['location']
    if not geocode: return search.raw['location']
    dis = vincenty((search.latitude, search.longitude), (geocode.latitude,
                                                         geocode.longitude)).m
    return search.raw['location'] if dis < 500 else geocode.raw['location']

def cut_city(name):
        n = jieba.cut(name)
        for c in n:
            if "县" in c or "区" in c or "市" in c:
                return c
        else:
            return None

def get_geo_data(name, place, city, item):
    cop = re.compile('\(.*\)')
    name = cop.sub('', name).strip()
    place = cop.sub('', place).strip()
    if not city:
        city = cut_city(name)
    if not city:
        city = cut_city(place)
    if not city:
        city = u"中国"

    data = get_geo_info(name, place, city=city)
    if not data:
        return False
    a = None
    for i in range(5):
        try:
            a = geo.reverse((data.latitude, data.longitude),
                            coordtype="gcj02ll", timeout=5)
            if a: break
        except Exception as e:
            logger.exception(e)
    item['location'] = {'lon': data.longitude, 'lat': data.latitude}
    if not a:
        return False
    res = a.raw['addressComponent']
    item['street'] = res['street']
    item['streetNumber'] = res['street_number']
    item['direction'] = res['direction']
    item['distance'] = res['distance']
    item['countryCode'] = res['country_code']
    item['adcode'] = res['adcode']
    if 'city' not in item or not item['city']:
        item['city'] = res['city']
    if 'district' not in item or not item['district']:
        item['district'] = res['district']
    if 'telephone' in data.raw and ('telephone' not in item or not item['telephone']):
        item['telephone'] = data.raw['telephone']
    if 'province' in res and ('province' not in item or not item['province']):
        item['province'] = res['province']
    return True

def get_geo(place):
    pass


def get_location_baidu_geo(location, item):
    url = location_reverse_url % (ak, location)
    r = requests.get(url)
    data = r.json()
    if "status" in data and data["status"] == 0:
        res = data['result']['addressComponent']
        item['district'] = res['district']
        item['street'] = res['street']
        item['streetNumber'] = res['street_number']
        item['direction'] = res['direction']
        item['distance'] = res['distance']
        item['countryCode'] = res['country_code']
        item['adcode'] = res['adcode']
        item['city'] = res['city']
        item['province'] = res['province']
        item['location'] = {'lon': res['location']['lng'],
                            'lat': res['location']['lat']}
    else:
        return False

def get_location_geo(location, item):
    for i in range(8):
        try:
            res = get_location_baidu_geo(location, item)
            if res: return True
        except Exception as e:
            logger.exception(e)
    else:
        return False

def get_ip_proxy():
    proxy_url = settings.get('IP_PROXY_URL')
    r = requests.get("%s?types=0" % proxy_url, timeout=30)
    return r.json()
