#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zhengwei
# email: zheng.weitt@gmail.com

import httplib,urllib, urllib2
import os,re
import decode 
import test

def myspider(chose):
    count = 1
    topid_list = ['/top/top500.html',
            '/top/top100.html',
            '/top/rihan.html',
            '/top/oumei.html',
            '/top/movie.html',
            '/top/duichang.html',
            '/top/yaogun.html',
            '/top/minyue.html',
            '/top/junlvminge.html']
    folder_list = ['top500',
            'top100',
            'rihan',
            'oumei',
            'movie',
            'duichang',
            'yaogun',
            'minyue',
            'junlvminge']
    
    match_list = [r'http://mp3.baidu.com/m\?rf=top-top500&tn=baidump3&ct=\d*&word=.*&lm=-1',
            r'http://mp3.baidu.com/m\?rf=top-oldsong&tn=baidump3&ct=.*&lm=-1',
            r'http://mp3.baidu.com/m\?rf=top-rihan&tn=baidump3&ct=.*&lm=-1',
            r'http://mp3.baidu.com/m\?rf=top-oumei&tn=baidump3&ct=.*&lm=-1',
            r'http://mp3.baidu.com/m\?rf=top-movie&tn=baidump3&ct=.*&lm=-1',
            r'http://mp3.baidu.com/m\?rf=top-duichang&tn=baidump3&ct=.*&lm=-1',
            r'http://mp3.baidu.com/m\?rf=top-yaogun&tn=baidump3&ct=.*&lm=-1',
            r'http://mp3.baidu.com/m\?rf=top-minyue&tn=baidump3&ct=.*&lm=-1',
            r'http://mp3.baidu.com/m\?rf=top-junlvminge&tn=baidump3&ct=.*&lm=-1']
    
    if chose<10 and chose>0:
        topid = topid_list[chose-1]
    else:
        topid = topid_list[0]
        chose = 1
    folder = folder_list[chose-1]
    
    errorlist = []
    conn = httplib.HTTPConnection('list.mp3.baidu.com')
    conn.request('GET',topid)
    response = conn.getresponse()
    html = response.read().decode('gb18030').encode('utf-8')
    conn.close()
    #match_site = re.compile(r'http://mp3.baidu.com/m\?rf=top-top500&tn=baidump3&ct=\d*&word=.*&lm=-1')
    match_site = re.compile(match_list[chose-1])
    site_list = match_site.findall(html)
 
    if not os.path.isdir(folder):
        os.system('mkdir ' + folder)
    song_singer = ''
    for site in site_list:
        try:
            conn = httplib.HTTPConnection('mp3.baidu.com')
            conn.request('GET',site)
            response = conn.getresponse()
            html = response.read().decode('gb18030').encode('utf-8')
            conn.close()
            song_singer_match = re.compile(r'<title>百度MP3搜索_.*</title>')
            s_s = song_singer_match.search(html)
            if s_s is not None:
                song_singer = s_s.group()[23:-8].strip()
            else:
                song_singer = ''
                print 'song and singer name not find'

            album = ''
            a_match = re.compile(r'<td class=al><a href="http://mp3.baidu.com/albumlist/.*</a>&nbsp;</td>')
            album_line = a_match.search(html)
            if album_line is not None:
                album_line = album_line.group()
                album_line = album_line.replace('</font>','')
                album_line = album_line.replace('<font color="#c60a00">','')
                a_match = re.compile(r'" target="_blank">.*</a>&nbsp;</td>$')
                album = a_match.search(album_line)
                if album is not None:
                    album = album.group()[18:-15]
                else:
                    album = 'noAlbumName'
            album = album.strip()
            song_singer_album = song_singer + '-' + album
            song_singer_album = song_singer_album.replace(' ','-')
 
            reg = r'http://\d*\.\d*\.\d*\.\d*/m\?word=\w*,http://.*&sgid=\d*'
            m = re.compile(reg)
            suburls_list = m.findall(html)
            
            song_singer_album = song_singer_album.replace(r'/','')
            song_singer_album = song_singer_album.replace(r':','')
            try:
                output = open(folder + os.sep + song_singer_album + '.txt', 'a')
            except:
                print song_singer_album + '.txt file open failed.' 
                continue
            print count, song_singer_album
            count += 1
            try:
                for mp3_suburl in suburls_list:
                    html = urllib.urlopen(mp3_suburl.decode('utf-8').encode('gb18030')).read().decode('gb18030')
                    conn.close()
                    sertim_match = re.compile(r'var sertim = \d*')
                    sertim = re.search(sertim_match, html).group()
                    sertim = sertim[13:]
                    sertim = int(sertim)
                    subulrs_match = re.compile('var subulrs = \[.*\]')
                    subulrs = re.search(subulrs_match, html).group()
                    subulrs = subulrs[15:-1]
                    subulrs = subulrs.split(',')

                    for j in range(len(subulrs)):
                        subulrs[j] = subulrs[j][subulrs[j].find('\"')+1:-1].encode('gb18030')
                    mp3_url_list = decode.get_urls(subulrs, sertim) #decode the baidu mp3 url
                    for mp3 in mp3_url_list:
                        if mp3 != '':
                            output.write(mp3+'\n')
            except:
                print 'url find error'
            output.close()
        except:
            print 'http connection error'
    
    print 'Succeed'
    
