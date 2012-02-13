# -*- coding: utf-8 -*-

import config
import helper.httper as http
import helper.jsoner as json
import random
import urllib


   
    
def getProgramsBySearch(key, page, size):
    if page is None or page < 0:
        page = 1        
    if size is None or size < 1:
        size = config.KANCHENE['size']
    start = (page - 1) * size
    params = _bulidSearchParams(key, start=start, rows = size)        
    content = http.get(config.KANCHENE['search_url'], params)
    if content is None:
        return None
        
    obj = json.decode(content)
    result = {}
    result['pageTotal'] = _getPageTotal(obj['response']['numFound'], size)
    result['page'] = page
    result['size'] = size
    result['time'] = obj['responseHeader']['QTime']
    result['total'] = obj['response']['numFound']
    result['data'] = obj['response']['docs']
    return result


def getProgramsByRelation(key, start, size):
    if start is None or start < 0:
        start = 1        
    if size is None or size < 1:
        size = config.KANCHENE['relation_size']
    params = _bulidSearchParams(key, start=start, rows = size)
    
    content = http.get(config.KANCHENE['search_url'], params)
    if content is None:
        return None
        
    obj = json.decode(content)
    result = obj['response']['docs']
    return result


def getProgramByID(pid):
    params = _bulidSearchByIDParams(pid, config.KANCHENE['relation_size'])
    content = http.get(config.KANCHENE['search_url'], params)
    if content is None:
        return None                
    obj = json.decode(content)
    if obj['response']['numFound'] < 1:
        return None
    program = {}
    program['program'] = obj['response']['docs'][0]
    program['relation'] = obj['moreLikeThis'][program['program']['id']]['docs']
    return program


def getProgramsByTopList(key, size):
    start = random.randint(0, 50)
    params = _bulidSearchParams(key, start = start, rows = size)
    content = http.get(config.KANCHENE['search_url'], params)
    #print 'content:%s' % content
    if content is None:
        return None
    obj = json.decode(content)
    return obj['response']['docs']
    

def _getPageTotal(total, size):
    return (total + size - 1)/size
    

def _bulidSearchParams(key, start, rows):
    return urllib.urlencode({'q': key, 'version': 2.2, 'start': start, 'rows': rows, 'indent': 'on', 'wt': 'json', 'sort': 'createDate desc'})

#http://192.168.6.66:9006/solr/select?indent=on&version=2.2&q=id:72934&start=0&rows=10&wt=json&mlt=true&mlt.boost=true&mlt.maxwl=5&mlt.maxqt=5&mlt.maxntp=5&mlt.fl=title,category,tag,description&mlt.count=12
def _bulidSearchByIDParams(pid, relationSize):
    key = 'id:%s' % pid
    return urllib.urlencode({'q': key, 'version': 2.2, 'start': '0', 'rows': '1', 'indent': 'on', 'wt': 'json', 'mlt': 'true', 'mlt.boost': 'true', 'mlt.maxwl': '5', 'mlt.maxqt': '5', 'mlt.maxntp': '5', 'mlt.fl': 'title,category,tag,description', 'mlt.count': relationSize})

