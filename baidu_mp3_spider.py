#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: Zhengwei

""" Get the mp3 in list.mp3.baidu.com.
    Use muti thread.
"""

__revision__ = '0.5'

import re, os, urllib2, xml, httplib
import baidu_mp3_decoder
import threading, Queue

class BaiduMp3Spider(threading.Thread):
    def __init__(self, indexQueue):
        threading.Thread.__init__(self)
        self.indexQueue = indexQueue
        self.topid = ''
        self.songs = ['', '']
        self.siteList = []
        self.songList = []
        self.singerList = []
        self.topMatch = r'http://mp3.baidu.com/m\?rf=top-index&tn=baidump3&ct=\d*&word=.*&lm=-1'
   
    def removeSame(self, seq):
        # Not order preserving
        return {}.fromkeys(seq).keys()

    def getMP3UrlList(self, songBoxList):
        '''
        Get mp3 url list
        '''
        mp3List = []
        for songBox in songBoxList:
            #print 'songBox', songBox
            try:
                html = urllib2.urlopen(songBox).read()
                #html = urllib2.urlopen(songBox.decode('utf-8').encode('gb18030').read().decode('gb18030').encode('utf-8'))
                baiduDecoder = baidu_mp3_decoder.BaiduMP3Decoder()
                urlList = baiduDecoder.decode(html)
                for u in urlList:
                    mp3List.append(u)
            except:
                print 'HTTP connection error, code 0x02'
                continue
        return self.removeSame(mp3List)

    def getSongBoxList(self, site):
        '''
        Get the songBox list of every song
        '''
        html = ''
        try:
            html = urllib2.urlopen(site.decode('utf-8').encode('gbk')).read().decode('gbk').encode('utf-8')
        except:
            print 'HTTP connection error, code 0x01'
            return None
        secondClassMatch = r'<td class="second">.*?</td>'
        secondMatch = re.compile(r'http://box\.zhangmen\.baidu\.com/m.*?"')
        secondList = secondMatch.findall(html)
        for i in range(len(secondList)):
            secondList[i] = secondList[i][0:-1]
        return secondList
        '''
        Finish get songBox list
        '''
    
    # read the index of the topid
    def getSiteList(self):
        conn = httplib.HTTPConnection('list.mp3.baidu.com')
        conn.request('GET', self.topid)
        response = conn.getresponse()
        html = response.read().decode('gb18030').encode('utf-8')
        conn.close()
        matchSite = re.compile(self.topMatch)
        self.siteList = matchSite.findall(html)
        return self.siteList

    # get the song and singer with 'site'
    def getSongSinger(self, site):
        tempList = site.split('&')
        songSinger = ''
        try:
            songSinger = tempList[3]
        except:
            print 'Out of range 1'
            return
        songSinger = songSinger.split('=')
        key = songSinger[1].replace('+', '-')
        return key


    # when single thread, use this
    def getSongSingerMp3(self):
        self.siteList = self.getSiteList() #get the site list in the chose site
        for site in self.siteList:
            key = self.getSongSinger(site) #get song and singer with 'site'
            songBoxList = self.getSongBoxList(site) #get songBox of the song, with read the site
            mp3List = self.getMP3UrlList(songBoxList) #get mp3List of the song, with read the songBoxList
            if mp3List is not None and mp3List != []:
                print 'name:', key
                print 'url', mp3List
    
    # when single thread, use this
    def getMp3s(self):
        topid_list = ['/top/top500.html', '/top/top100.html']
        folderList = ['Top500', 'Top100']
        print '0: Top 500'
        print '1: Top 100'
        chose = raw_input('You chose: ')
        self.topid = topid_list[int(chose) % 2]
        if not os.path.isdir('Baidu_MP3'):
            os.system('mkdir Baidu_MP3')
            os.system('mkdir -p Baidu_MP3/' + folderList[int(chose)%2])
        print 'Start...'
        self.getSongSingerMp3()
        print 'End.'
    
    def run(self):
        while True:
            site = indexQueue.get()
            if site is None or site=='':
                continue
            key = self.getSongSinger(site) # read the song and singer
            songBoxList = self.getSongBoxList(site) #read the songBoxList
            if songBoxList is None:
                continue
            mp3List = self.getMP3UrlList(songBoxList) # read the mp3List
            if mp3List is not None and mp3List != []:
                #print 'name:', key
                #print 'url:', mp3List
                fileName = folder + os.sep + key + '.txt'
                print fileName
                out = open(fileName, 'a')
                for url in mp3List:
                    print >> out, url
                out.close()
            self.indexQueue.task_done()

indexQueue = Queue.Queue()
folder = 'Baidu_mp3'

def main():
    print 'Starting...'
    if not os.path.isdir(folder):
        os.system('mkdir ' + folder)

    baiduMp3Spider = BaiduMp3Spider(indexQueue)
    indexList = baiduMp3Spider.getSiteList()
    for index in indexList:
        indexQueue.put(index)
    
    for i in range(10):
        print 'Creating thread ', i+1
        t = BaiduMp3Spider(indexQueue)
        t.setDaemon(True)
        t.start()

    indexQueue.join()
    print 'Main thread exit.'

if __name__ == '__main__':
    main()

