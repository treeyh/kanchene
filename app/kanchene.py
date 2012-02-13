#-*- encoding: utf-8 -*-

import tornado.web
import tornado.escape
import random
import config
import redis
import models
from datetime import datetime
import helper.jsoner as json

indexlist = ['chezhan', 'meinv', 'xinche', 'piaoyi', 'guanggao']
toplist = ['wanche', 'biaoche', 'bisai', 'guanggao']

cachePool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
cacheKey = 'kanchene_index_top_'


class BaseHandler(tornado.web.RequestHandler):    
    def get_current_user(self):
        return None


class IndexHandler(BaseHandler):
    def get(self):
        ps = config.KANCHENE
        ps['title'] = '%s%s' % ('首页', ps['pagetitle'])
        ps['date'] = datetime.now()        
        ps['top'] = {}
        ps['desc'] = ''
        r = redis.Redis(connection_pool=cachePool)
        key = '%smain' % (cacheKey)        
        ps['show'] = r.get(key)
        if None == ps['show']:
            show = models.getProgramByID(363736)
            ps['show'] = show['program']
        else:
            ps['show'] = json.decode(ps['show'])[0]
        for top in toplist:
            key = '%s%s' % (cacheKey, top)
            programList = r.get(key)
            if None == programList:
                ps['top'][top] = models.getProgramsByTopList(config.KANCHENE['channel_key'][top], 10)
            else:
                ps['top'][top] = json.decode(programList)
            ps['top'][top] = formatProgram(ps['top'][top], 35)            
        ps['index'] = {}
        for index in indexlist:
            page = random.randint(1, 50)
            ps['index'][index] = models.getProgramsBySearch(config.KANCHENE['channel_key'][index], page, 8)
            ps['index'][index]['data'] = formatProgram(ps['index'][index]['data'], 20)
        self.render("index.htm", **ps)


class ListHandler(BaseHandler):
    def get(self, key, page):
        ps = config.KANCHENE
        ps['date'] = datetime.now()
        key = key.encode('utf-8')
        ps['desc'] = ''
        if key not in ps['channel_key']:
            ps['keyword'] = key
            ps['urlpre'] = '%ss/%s/' % (ps['domain'], tornado.escape.url_escape(key))
        else:
            ps['keyword'] = ps['channel_key'][key]
            ps['urlpre'] = '%s%s/' % (ps['domain'],tornado.escape.url_escape(key))
        if page == '': page = '1'
        if page is not None: page = int(page)
        ps['data'] = models.getProgramsBySearch(ps['keyword'], page, ps['size'])
        ps['data']['data'] = formatProgram(ps['data']['data'], 20)
        if ps['keyword'] == '*':
            ps['keyword'] = '全部视频'
        ps['title'] = '%s%s' % (ps['keyword'], ps['pagetitle'])
        ps['pageArea'] = getPageNumArea(ps['data']['pageTotal'], ps['data']['page'])
        self.render("list.htm", **ps)


class PlayHandler(BaseHandler):
    def get(self, id):
        ps = config.KANCHENE
        ps['date'] = datetime.now()
        if id is not None: id = int(id)
        programInfo = models.getProgramByID(id)      
#        print 'programInfo:%s' % programInfo['program']      
        if programInfo is None:
            ps['title'] = '%s%s' % ('播放页', ps['pagetitle'])
            ps['data'] = None
            ps['desc'] = ''
            ps['cats'] = []
            ps['relations'] = {}
        else:
            ps['data'] = programInfo['program']
            ps['desc'] = ps['data']['description']
            ps['title'] = '%s%s' % (programInfo['program']['title'].encode("UTF-8"), ps['pagetitle'])
            ps['cats'] = programInfo['program']['category'].split(',')
            ps['relas'] = programInfo['relation']
            ps['data']['swf'] = getAutoPlayUrl(ps['data'])
        self.render("play.htm", **ps)
        
class ErrorHandler(BaseHandler):
    def get(self):
        ps = config.KANCHENE
        ps['date'] = datetime.now()
        ps['title'] = '页面无法找到'
        ps['desc'] = '页面无法找到'
        self.render("error.htm", **ps)


def getPageNumArea(pageTotal, page):
    count = 7
    numArea = []
    middleNum = (count / 2) + 1      
    if page <= middleNum:    
        for i in range(1, count+1):
            if i > pageTotal: break;
            numArea.append(i)
    elif (page >= (pageTotal - count + middleNum)):
        for i in range(1, count+1):
            if i > pageTotal: break;
            numArea.append(pageTotal - count + i)
    else:
        for i in range(1, count+1):
            if i > pageTotal: break;
            numArea.append(page - middleNum + i)
    return numArea

def getAutoPlayUrl(p):
    url = p['swf']
    if p['site'] == 'youku':
        url = 'http://player.youku.com/player.php/sid/%s/v.swf?VideoIDS=%s&isAutoPlay=true&isShowRelatdVideo'  % (p['sourceID'] , p['sourceID'])
    elif p['site'] == 'tudou':
        if '/v.swf'  in  url:
            url = url.replace('/v.swf', '&autoPlay=true/v.swf')
        else:
            url = '%s%s' % (url, '&autoPlay=true/v.swf')
    return url

def formatProgram(ps, titlecount):    
    if isinstance(ps, list):
        for p in ps:
            p['showtitle'] = p['title'] if len(p['title']) <= titlecount else ('%s...' % p['title'][0:titlecount])
    else:
        ps['showtitle'] = ps['title'] if len(ps['title']) <= titlecount else ('%s...' % ps['title'][0:titlecount])
    return ps
