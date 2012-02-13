#-*- encoding: utf-8 -*-

import os
import kanchene
import kancheneadmin

#"static_path": os.path.join(os.path.dirname(__file__), "static"),
#    "template_path":os.path.join(os.path.dirname(__file__), "templates"),    


route = []
route.append((r'^/$', kanchene.IndexHandler))
route.append((r'^/(zixun|chezhan|meinv|redian|xuanche|shijia|saiche|wanche|piaoyi|guanggao|paoche|all)[/]{0,1}(\d{0,})$', kanchene.ListHandler))
route.append((r'^/(zixun|chezhan|meinv|redian|xuanche|shijia|saiche|wanche|piaoyi|guanggao|paoche|all)[/]{0,1}(\d{0,}).htm$', kanchene.ListHandler))
route.append((r'^/s/([^\.\/]{1,})[/]{0,1}(\d{0,}).htm$', kanchene.ListHandler))
route.append((r'^/v/(\d{0,}).htm$', kanchene.PlayHandler))


route.append((r'^/admin/login.htm', kancheneadmin.LoginHandler))
route.append((r'^/admin/loginout.htm', kancheneadmin.LoginOutHandler))
route.append((r'^/admin/logindo.htm', kancheneadmin.LoginDoHandler))
route.append((r'^/admin/index.htm', kancheneadmin.IndexHandler))
route.append((r'^/admin/', kancheneadmin.IndexHandler))
route.append((r'^/admin/search.htm$', kancheneadmin.SearchHandler))





KANCHENE = {
    'sitename' : '看车呢',
    'pagetitle' : ' - 看车呢 - 提供专业汽车,车展,美女,选车,新车视频搜索在线观看服务',
    'search_url' : 'http://127.0.0.1:9006/solr/select?%s',
    'domain' : 'http://www.kanchene.com.cn/',
    'jsdomain' : 'http://css.tv189.cn/css/kcn/js/',
    'cssdomain' : 'http://css.tv189.cn/css/kcn/css/',
    'imgdomain' : 'http://css.tv189.cn/css/kcn/images/',
    'path' : '/opt/www/kanchene_tornado/app/',
    'size' : 30,
    'relation_size' : 12,
    'version':'3',
    'channel_key' : {
        'zixun' : '车讯',
        'chezhan' : '车展',
        'meinv' : '车展美女',
        'redian' : '热点',
        'xuanche' : '选车',
        'shijia' : '试驾',
        'saiche' : '赛车',
        'wanche' : '玩车',
        'piaoyi' : '漂移',
        'guanggao' : '广告',
        'paoche' : '跑车',
        'chezhan': '车展',
        'xinche': '新车',        
        'biaoche' : '飙车',
        'bisai' : '比赛',
        'all' : '*',
    },
}

CACHE = {
    'host' : '127.0.0.1',
    'port' : 6379,
    'db' : 0,
    'time_out' : 7776000,
}



#os.path.join(os.getcwd(), 'templates').replace('\\','/'),
settings = dict(
    login_url = '/login',
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    #xsrf_cookies=True,
    cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",    
    debug=True,
)
