#-*- encoding: utf-8 -*-

import tornado.web
import tornado.escape
import random
import config
import redis
import models
import kanchene
import helper.jsoner as json
from datetime import datetime

class BaseHandler(tornado.web.RequestHandler):    
    def get_current_user(self):
        return self.get_secure_cookie('user')
        
class LoginHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        ps = config.KANCHENE
        ps['title'] = '%s%s' % ('用户登录 - 后台', ps['pagetitle'])
        ps['date'] = datetime.now()        
        ps['desc'] = ''
        ps['action'] = '%sadmin/logindo.htm' % ps['domain']
        self.render('admin/login.htm', **ps)

class LoginDoHandler(BaseHandler):
    def post(self):
        user = self.get_argument('user', '')
        password = self.get_argument('password', '')
        if 'tree' == user and 'dswybs' == password:
            self.set_secure_cookie('user', 'tree')
            self.redirect('%sadmin/index.htm' % (config.KANCHENE['domain']))
        else:
            self.redirect('%sadmin/login.htm' % (config.KANCHENE['domain']))    

class LoginOutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect('%sadmin/login.htm' % (config.KANCHENE['domain']))

class IndexHandler(BaseHandler):
    def get(self):
        if 'tree' != self.get_current_user():
            self.redirect('%sadmin/login.htm' % (config.KANCHENE['domain']))
            return
        ps = config.KANCHENE
        ps['desc'] = ''
        ps['title'] = '%s%s' % ('欢迎访问 - 后台', ps['pagetitle'])
        self.render('admin/index.htm', **ps)
    
    def post(self):
        type = self.get_argument('videoType','')
        ids = self.get_argument('videoIDs', '')
        ps = config.KANCHENE
        ps['desc'] = ''
        ps['title'] = '%s%s' % ('欢迎访问 - 后台', ps['pagetitle'])
        if '' == ids:
            ps['error'] = 'ids is null'
            self.redirect('%sadmin/index.htm?msg=no' % (config.KANCHENE['domain']))
            return
        key = '%s%s' % (kanchene.cacheKey, type)
        searchkey = 'id:(%s)' % ids.replace(',', ' ')
        ps = models.getProgramsByKey(searchkey, 0, 10)
	#print ps
        programList = []
        for i in ids.split(','):
            if None == i or '' == i:    
                continue
            for p in ps:
                if int(i) != p['id']:
                    continue
                programList.append(p)
                break
        js = tornado.escape.json_encode(programList)
	#print programList
	#print js
        r = redis.Redis(connection_pool=kanchene.cachePool)
        r.setex(key, time =config.CACHE['time_out'], value = js)
        self.redirect('%sadmin/index.htm?msg=ok' % (config.KANCHENE['domain']))
        

class SearchHandler(BaseHandler):
    def get(self):
        if 'tree' != self.get_current_user():
            self.redirect('%sadmin/login.htm' % (config.KANCHENE['domain']))
            return
        ps = config.KANCHENE
        ps['desc'] = ''
        ps['title'] = '%s%s' % ('视频搜索 - 后台', ps['pagetitle'])
        key = self.get_argument('q', '')
        page = int(self.get_argument('page', '1'))
        if '' == key or 'main' == key:
            ps['keyword'] = self.get_argument('txtKey', '*').encode('utf-8')
        else:
            ps['keyword'] = ps['channel_key'][key]
        ps['data'] = models.getProgramsBySearch(ps['keyword'], page, 50)
        ps['page'] = page
        self.render('admin/search.htm', **ps)



