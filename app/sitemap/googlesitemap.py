#-*- encoding: utf-8 -*-


import sys
import os
import codecs
import random
import datetime
import tarfile

mappath = '%s/../' % (os.getcwd())
sys.path.append(mappath)
import config
import models

def buildSitemap():
    page = 1
    ps = models.getProgramsBySearch('*', page, 10000)
    pageTotal = ps['pageTotal']    
    formatSiteMap(ps['data'], page)
    for i in range(2, pageTotal + 1):
        ps = models.getProgramsBySearch('*', i, 10000)
        formatSiteMap(ps['data'], i)
    sitemapindex(pageTotal)
    print 'over'
    

def formatSiteMap(data, page):
    xml = '<?xml version="1.0" encoding="UTF-8" ?>'
    xml = '%s<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">' % xml
    index = 0
    for p in data:
        index = index + 1
        print '%s_%s' % (page, index)
        xml = '%s<url><loc>%sv/%s.htm</loc>' % (xml, config.KANCHENE['domain'], p['id'])
        xml = '%s<video:video><video:thumbnail_loc>%s</video:thumbnail_loc>' % (xml, p['cover'])
        xml = '%s<video:title><![CDATA[%s]]></video:title>' % (xml, p['title'])
        xml = '%s<video:description><![CDATA[%s]]></video:description>' % (xml, p['description'])
        xml = '%s<video:player_loc allow_embed="yes">%s</video:player_loc>' % (xml, p['swf'])
        xml = '%s<video:duration>%s</video:duration>' % (xml, p['timeLengthInt'])
        xml = '%s<video:rating>4.%s</video:rating>' % (xml, random.randint(0,99))
        #xml = '%s<video:view_count>%s</video:view_count>' % (xml, '1000')
        xml = '%s<video:publication_date>%s+08:00</video:publication_date>' % (xml, p['createDate'].replace(' ', 'T'))
        tags = p['tags'].split(',')
        for t in tags:
            if None == t or '' == t:
                continue
            xml = '%s<video:tag>%s</video:tag>' % (xml, t)
        cat = p['category'] 
        if None == cat or cat != '':
            cat = p['channelName']
        xml = '%s<video:category>%s</video:category>' % (xml, cat)
        xml = '%s<video:live>no</video:live>' % xml
        xml = '%s</video:video></url>' % xml
    xml = '%s</urlset>' % xml
    filename = '%s../sitemap/google_sitemap_%s.xml' % (mappath, page)    
    file_object = codecs.open(filename, 'w', 'utf-8')
    file_object.write(xml)
    file_object.close()
    shell = 'cd %s../sitemap/; tar -zcvf google_sitemap_%s.xml.tar.gz google_sitemap_%s.xml' % (mappath, page, page)
    os.system(shell)
    
    
def sitemapindex(pageTotal):
    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    xml = '%s<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' % xml
    for i in range(1, pageTotal+1):
        xml = '%s<sitemap><loc>%ssitemap/google_sitemap_%s.xml.tar.gz</loc>' % (xml, config.KANCHENE['domain'], i)
        xml = '%s<lastmod>%s+08:00</lastmod></sitemap>' % (xml, datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    xml = '%s</sitemapindex>' % xml
    filename = '%s../sitemap/google_sitemap.xml' % (mappath)    
    file_object = codecs.open(filename, 'w', 'utf-8')
    file_object.write(xml)
    file_object.close()
    
        


if __name__ == '__main__':
    buildSitemap();


