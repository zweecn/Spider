#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: Zhengwei

"""docstring
"""

__revision__ = '0.1'

import re, urllib2, xml, httplib

class BaiduMp3Spider:
    def __init__(self, topid):
        self.songs = ['', '']
        self.topid = topid
        self.siteList = []
        self.songList = []
        self.singerList = []
        self.songSingerDict = {}
        self.topMatch = r'http://mp3.baidu.com/m\?rf=top-index&tn=baidump3&ct=\d*&word=.*&lm=-1'

    def getTopUrlList(self):
        conn = httplib.HTTPConnection('list.mp3.baidu.com')
        conn.request('GET', self.topid)
        response = conn.getresponse()
        html = response.read().decode('gb18030').encode('utf-8')
        conn.close()
        matchSite = re.compile(self.topMatch)
        self.siteList = matchSite.findall(html)
        for site in self.siteList:
            tempList = site.split('&')
            songSinger = ''
            try:
                songSinger = tempList[3]
            except:
                print 'Out of range 1'
                continue

            songSinger = songSinger.split('=')
            key = songSinger[1].replace('+', '-')
            self.songSingerDict[key] = []
            
            html = ''
            try:
                html = urllib2.urlopen(site.decode('utf-8').encode('gbk')).read().decode('gbk').encode('utf-8')
            except:
                print 'HTTP connection error.'
                continue

            secondClassMatch = r'<td class="second">.*?</td>'
            secondMatch = re.compile(r'http://box\.zhangmen\.baidu\.com/m.*?"')
            secondList = secondMatch.findall(html)
            for i in range(len(secondList)):
                secondList[i] = secondList[i][0:-1]
            '''
            print 'secondList', secondList
            matchClass = re.compile(secondClassMatch)
            secondClassList = matchClass.findall(html)
            print 'secondClassList', secondClassList
            songMatch = r'http://box.zhangmen.baidu.com/m?word=mp3,,,.*'
            '''
            for songBox in secondList:
                print 'songBox', songBox
                '''
                doc = xml.dom.minidom.parseString(songBox)
                aNode = searchDoc.getElementsByName('a')
                href = aNode.getAttribute('href')
                print 'href', href
                '''
                try:
                    html = urllib2.urlopen(songBox).read()
                    #html = urllib2.urlopen(songBox.decode('utf-8').encode('gb18030').read().decode('gb18030').encode('utf-8'))
                    print html
                    return
                except:
                    print 'HTTP connect error.'
                    return
            


if __name__ == '__main__':
    print 'begin...'
    topid = '/top/top500.html'
    baiduSpider = BaiduMp3Spider(topid)
    baiduSpider.getTopUrlList()
