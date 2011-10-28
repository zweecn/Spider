#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: Zhengwei

"""docstring
"""

__revision__ = '0.1'

import re, os

class BaiduMP3Decoder:
    def __init__(self):
        self.strList = []
    
    def urlM(self, url):
        url = url.replace("zhangmenshiting.","zhangmenshiting2.")
        return url
    
    def findSubulrs(self, html):
        subulrsMatch = re.compile(r'var\ subulrs\ *=\ *\[urlM\(.*?\)')
        subulrsList = subulrsMatch.findall(html)
        subulrsListRes = []
        for sub in subulrsList:
            url = sub[sub.find('(')+1:sub.find(')')]
            aPartUrlList = url.split('+')
            url = ''
            for p in aPartUrlList:
                url += p.strip()[1:-1]
            subulrsListRes.append(url)
        return subulrsListRes
    
    def readFile(self, fileName):
        inFile = open(fileName, 'r')
        html = inFile.read()
        return html
        
    def decode(self, html):
        subulrs = []
        subulrsList = self.findSubulrs(html)
        for sub in subulrsList:
            subulrs.append(self.urlM(sub))
        self.strList = []
        for sub in subulrs:
            if sub is not None:
                self.strList.append(sub)
        return self.strList
        '''
        #subulrs = [urlM('http://zhangmens' + 'hiting.baidu.com/data/music/5945' + '602' + '/%E8%B5%B0' + '%E5%A4%A9%E6%B6%AF.mp3?xcode=2a98c5ff' + 'bd0' + '9d1e5bd20ec4344f25e6f'), urlM('h' + 'ttp:/' + '/h' + 'w828.c' + 'o' + 'm/' + '001.mp3'), urlM('http://www.hinews.cn/a' + 'udio/0/10/35/34/10353479_642484.mp3?autorep' + 'lahttp:/' + '/www.dodecms.com/mp3/zoutianya.mp3'), urlM('http://z' + 'hangmenshiti' + 'ng4.baidu' + '.com/cdn/baidump3/20110829/music/597' + '4988.mp3?xcode=38e4c81a4d80c' + '024674e52aa74965028')]
        #subulrs_s = [urlM("http://zhangmenshiting.baidu.com/...344f25e6f"),urlM("http://hw828.com/001.mp3"),urlM("http://www.hinews.cn/...com/mp3/zoutianya.mp3"),urlM("http://zhangmenshiting4.baidu.com/...74965028")]
        #self.str = ""
        for sub in subulrs:
            if sub is not None:
                subcnt++
                if (subcnt > 1):
                    self.str += "<br>"
                self.str += "<a target='_blank' href='" + subulrs[k] + "' onmousedown='sd(event," + subcnt + ",this);'>" +subulrs_s[k] + "</a>"
        ''' 
if __name__=='__main__':
    baiduDecoder = BaiduMP3Decoder()
    html = baiduDecoder.readFile(r'1.log')
    urlList = baiduDecoder.decode(html)
    for url in urlList:
        print url

