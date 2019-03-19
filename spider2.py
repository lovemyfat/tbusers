# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 16:04:48 2019

@author: yyzq135
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:51:53 2019

@author: yyzq135
"""

import json
import re
from multiprocessing import Pool
import requests
from requests import RequestException
from lxml import etree
'''
import io
import sys
import urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
'''

def get_cookies(cookie_str):
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        key = key.strip()
        cookies[key] = value
    return cookies

def get_html(url, cookies):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}  
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            return response.content.decode('utf8', errors='ignore')
        return None
    except RequestException:
        print('打开原始页失败')
        return None

def parse_html_order(html):#//*[@id="nick_979"]
    if html:
        selector = etree.HTML(html)
        pattern_all = re.compile('<span id=.*?>(.*?)<\/span>', re.S)
        title = re.findall(pattern_all, html)
        pattern_img = re.compile('<(img.*)>', re.S)
        #x.replace(re.findall(pattern_img, x)[0], '')
        title = [x.replace(re.findall(pattern_img, x)[0], '')[:-2] if re.findall(pattern_img, x) else x for x in title]
        #title = selector.xpath('//table/tbody/tr/td/p/span//*/text()')
        uid = selector.xpath('//table/tbody/tr/td[4]/p[1]//text()')
        #uid = selector.xpath('//table[@class="layui-table"]/tbody/tr/td[3]/p[1]/*[1]/text()')
        group = selector.xpath('//table/tbody/tr/td[4]/p[2]/text()')
        num = selector.xpath('//table/tbody/tr/td[4]/p[3]/text()')
        remain = selector.xpath('//table/tbody/tr/td[5]/p[1]/text()')
        credit = selector.xpath('//table/tbody/tr/td[5]/p[2]/text()')
        value = selector.xpath('//table/tbody/tr/td[5]/p[3]/text()')
        invator = selector.xpath('//table[@class="layui-table"]/tbody/tr/td[7]//text()')
        follow_date = selector.xpath('//table[@class="layui-table"]/tbody/tr/td[8]/p[1]//text()')
        cancel_date = selector.xpath('//table[@class="layui-table"]/tbody/tr/td[8]/p[2]//text()')
        status = selector.xpath('//table[@class="layui-table"]/tbody/tr/td[8]/p[3]//text()')
        #return rebate_date
        uid = [x.strip()[4:] for x in uid if 'UID' in x]
        if len(title)==len(uid)==len(group)==len(num)==len(remain)==len(credit)==len(value)==len(invator)==len(follow_date)==len(cancel_date)==len(status):
            orders = zip(title, uid, group, num, remain, credit, value, invator, follow_date, cancel_date, status)
            print('真好')
            for order in orders:
                yield (
                            order[0],
                            order[1],
                            order[2],
                            order[3],
                            order[4],
                            order[5],
                            order[6],
                            order[7],
                            order[8],
                            order[9],
                            order[10]
                            )
        else:
            print('当前网页元素有缺失')
            print({'title': len(title),
                        'uid': len(uid),
                        'group': len(group),
                        'num': len(num),
                        'remain': len(remain),
                        'credit': len(credit),
                        'value': len(value),
                        'invator': len(invator),
                        'follow_date': len(follow_date),
                        'cancel_date': len(cancel_date),
                        'status': len(status)
                        })
            return False
        '''
        for order in orders:
            yield {
                        'title': order[0],
                        'uid': order[1][5:-1],
                        'order_num': order[2],
                        'status': order[3],
                        'pay': order[4][1:],
                        'commision': order[5],
                        'rebate': order[6][1:],
                        'purchase_date': order[7],
                        'close_date': order[8],
                        'rebate_date': order[9],
                        }
            '''

def get_next_page(html):#//*[@id="layui-laypage-6"]/a[13]
    if html:
        selector = etree.HTML(html)
        diagnose = selector.xpath('//*[@id="layui-laypage-6"]/a[@class="layui-laypage-next"]/text()')
        print(diagnose)
        return diagnose
    
def get_order_detail(html, url, cookies):
    page = 1
    while True:
        complete_url = url + str(page)
        html = get_html(complete_url, cookies)
        info = parse_html_order(html)
        for title, uid, info_list in info:
            pass
        if get_next_page(html):
            page += 1
        else:
            break

def file_clear_title(content):
    with open('user_info.csv', 'w+', encoding='utf-8') as f:
        for col in content:
            f.write(json.dumps(col, ensure_ascii=False) + ',')
        f.write('\n')
        f.close()
    
def write_to_file(content):
    with open('user_info.csv', 'a', encoding='utf-8') as f:
        for row in content:
            for grid in row:
                f.write(json.dumps(grid, ensure_ascii=False) + ',')
            f.write('\n')
        f.close()

def main():
    cookie_str = r'aid=264; aname=sqxjl; apass=3d9188577cc9bfe9291ac66b5cc872b7; starttime=1550731218; endtime=1582267218; edition=1; iden=sqxjl'
    user_url = 'http://sqxjl.du29s.cn/admin.php/user/user?p='
    #'http://sqxjl.du29s.cn/admin.php/user/user?p=3'
    '''
    cookies = get_cookies(cookie_str)
    page = 8
    url = user_url + str(page)
    html = get_html(url, cookies)
    info = parse_html_order(html)
    for x in info:
        print(x)
        
    '''
        #write_to_file(x)
    cookies = get_cookies(cookie_str)
    cols_name = ['昵称','用户ID','分组','手机','余额','积分','会员值','邀请人','关注时间','取关时间', '当前状态']
    file_clear_title(cols_name)
    page = 1
    while True:
        completed_url = user_url + str(page)
        print(completed_url)
        html = get_html(completed_url, cookies)
        info = parse_html_order(html)
        if info:
            write_to_file(info)
        next_page = get_next_page(html)
        if next_page:
            page += 1
        else:
            break

if __name__ == '__main__':
    main()
    #pool = Pool()
    #pool.map(main, [i*10 for i in range(10)])


    