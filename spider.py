# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 10:51:53 2019

@author: yyzq135
"""

import json
from multiprocessing import Pool
import requests
from requests import RequestException
from lxml import etree

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

def parse_html_order(html):
    if html:
        selector = etree.HTML(html)
        title = selector.xpath('//table/tbody/tr/td/p/a[@target="_blank"]/text()')
        uid = selector.xpath('//table/tbody/tr/td[3]/p[1]/a[@style="color:#01AAED;"]/text()|//table[@class="layui-table"]/tbody/tr/td[3]/p[1]/font[@color="#d2d2d2"][1]/text()')
        #uid = selector.xpath('//table[@class="layui-table"]/tbody/tr/td[3]/p[1]/*[1]/text()')
        order_num = selector.xpath('//table/tbody/tr/td[3]/p[2]/text()')
        status = selector.xpath('//table/tbody/tr/td[3]/p[3]/text()|//table/tbody/tr/td[3]/p[3]/font//text()')
        pay = selector.xpath('//table[@class="layui-table"]/tbody/tr/td[4]/p[1]/text()')
        commision = selector.xpath('//table[@class="layui-table"]/tbody/tr/td[4]/p[2]/text()')
        rebate = selector.xpath('//table[@class="layui-table"]/tbody/tr/td[4]/p[3]/text()')
        purchase_date = selector.xpath('//table[@class="layui-table"]/tbody/tr/td[5]/p[1]/text()')
        #close_date = selector.xpath('//table[@class="layui-table"]/tbody/tr/td[5]/p[2]//text()')
        rebate_date = selector.xpath('//table[@class="layui-table"]/tbody/tr/td[5]/p[3]//text()')
        #return rebate_date
        if len(title)==len(uid)==len(order_num)==len(status)==len(pay)==len(commision)==len(rebate)==len(purchase_date)==len(rebate_date):
            orders = zip(title, uid, order_num, status, pay, commision, rebate, purchase_date, rebate_date)
            for order in orders:
                yield (
                            order[0],
                            order[1][5:-1],
                            order[2],
                            order[3],
                            order[4][1:],
                            order[5],
                            order[6][1:],
                            order[7],
                            order[8]
                            )
        else:
            print('当前网页元素有缺失')
            print({'title': len(title),
                        'uid': len(uid),
                        'order_num': len(order_num),
                        'status': len(status),
                        'pay': len(pay),
                        'commision': len(commision),
                        'rebate': len(rebate),
                        'purchase_date': len(purchase_date),
                        #'close_date': len(close_date),
                        'rebate_date': len(rebate_date)})
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

def get_next_page(html):
    if html:
        selector = etree.HTML(html)
        diagnose = selector.xpath('//a[@class="layui-laypage-next"]/text()')
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
    with open('result.csv', 'w+', encoding='gbk') as f:
        for col in content:
            f.write(json.dumps(col, ensure_ascii=False) + ',')
        f.write('\n')
        f.close()
    
def write_to_file(content):
    with open('result.csv', 'a', encoding='gbk') as f:
        for row in content:
            for grid in row:
                f.write(json.dumps(grid, ensure_ascii=False) + ',')
            f.write('\n')
        f.close()

def main():
    cookie_str = r'aid=264; aname=sqxjl; apass=3d9188577cc9bfe9291ac66b5cc872b7; starttime=1550731218; endtime=1582267218; edition=1; iden=sqxjl'
    order_url = ['http://sqxjl.du29s.cn/admin.php/taoke/tkorder?p=',
                 'http://sqxjl.du29s.cn/admin.php/pdd/pddorder?p=']
    #tb_url = 'http://sqxjl.du29s.cn/admin.php/taoke/tkorder?p='
    #'http://sqxjl.du29s.cn/admin.php/user/user?p=3'
    '''
    cookies = get_cookies(cookie_str)
    page = 3
    url = tb_url + str(page)
    html = get_html(url, cookies)
    info = parse_html_order(html)
    print(len(info), info)
    i =0
    for x in info:
        print(x)
        i += 1
    print(i)
    '''
        #write_to_file(x)
    cookies = get_cookies(cookie_str)
    cols_name = ['标题','用户ID','订单编号','订单状态','实付','佣金比例','返利','创建时间','返利时间']
    file_clear_title(cols_name)
    for url in order_url:
        page = 1
        while True:
            completed_url = url + str(page)
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


    