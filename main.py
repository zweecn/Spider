#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zhengwei
# email: zheng.weitt@gmail.com

import httplib,urllib, urllib2
import os,re
import decode,spider 
import test

if __name__=='__main__':
    print '''
选择要爬行的网页:
    [0] 以下全部歌曲
    [1] 歌曲TOP500
    [2] 新歌TOP100
    [3] 日韩流行风
    [4] 欧美金曲
    [5] 影视金曲
    [6] 热门对唱
    [7] 摇滚歌曲榜
    [8] 中国民乐
    [9] 流金岁月
'''

    chose = raw_input('你的选择: ')
    chose = int(chose)
    if chose==0:
        for chose in range(1,10):
            spider.myspider(chose)
    else:
        spider.myspider(chose)

