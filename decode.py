#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: zhengwei 
# email: zheng.weitt@gmail.com

def get_urls(subulrs, sertim):
    str = []
    subcnt = 0
    for x in subulrs:
        if x is not None:
            str.append(decode(x, sertim))
    return str

def init(head, bottom, middle, asc_arr1, asc_arr2):
    for i in range(head,bottom+1):
        asc_arr1[i] = i + middle
        asc_arr2[i+middle] = i

def decode(url, sertim):
    length = len(url)
    decurl = ''
    key = sertim % 26
    if key==0:
        key = 1
    asc_arr1 = {}
    asc_arr2 = {}
    init(0, 9, 48, asc_arr1, asc_arr2)
    init(10, 35, 55, asc_arr1, asc_arr2)
    init(36, 61, 61, asc_arr1, asc_arr2)
    for i in range(length):
        word = url[i]
        if word.isalpha() or word.isdigit():
            pos = asc_arr2[ord(url[i])] - key  #
            if pos<0:
                pos += 62
            word = asc_arr1[pos] ##
            word = chr(word)
        decurl += word
    return decurl

if __name__=='__main__':
    sertim = 1271510093
    s2 = 1271948228
 #   subulrs = ["q22y://8qjwpvnw1qr2rwp.kjrm3.lxv/1n04rln/oEloFCGHnjEEEDkmkABBmAEHD9jHnkAn.vyC?6lxmn=jBBlkHlCCmjjDjljkkAmlBmICGBmmFIGCH", "q22y://xumkuxp.4xl.lxv.lw/1yA/ur3lqjwplq3w/v31rl/AAGGEIAFBDC9G_G9EF.5vj", "q22y://lx301n.zzq03.nm3.lw/nxu/qxvnyjpn/zzq03/lx301n5j0n/9E9A9A/d/GI/j3mrx/pjx1qjw.vyC", "q22y://555.5zq3wsrj.lxv/v31rl/vyC/jr.vyC"]

    s = ["zBB7://Hzs5y4w5Az0B05y.ts0vC.u64/Aw9D0uw/OtNOxtKQRwKRRQKtKtItKtRQxxPNQvMQ.47L?Fu6vw=vxvtIIJvwxJONIRQxwIKQPssIsKNtwRuKO", "zBB7://yu2BD.NJ402w.u64/4CA0ux03w/KIIQJKKN/JIIIIKIJMJUZgiqV.E4s", "zBB7://EEE.7s9BGB6E5.u64.u5/ty4CA0u.47L", "zBB7://Cu5.88v0ywAB.u64/7899C9B7/ACF.47L"];
    
    urls = get_urls(s, s2)
    print urls
