# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/2/2--21:19
__author__ = 'Henry'

'''
爬取B站直播弹幕并发送跟随弹幕
'''

import requests, re
import time
import random


def main():
    print('*' * 30 + '欢迎来到B站直播弹幕小助手' + '*' * 30)
    url = input('请输出您要查看的直播房间网址链接:')
    cookie = input('请输入账号登录后的Cookie值:')
    token = re.search(r'bili_jct=(.*?);', cookie).group(1)
    # 获取roomid
    html = requests.get(url).text
    if re.search(r'room_id":(.*?),', html):
        roomid = re.search(r'room_id":(.*?),', html).group(1)
        print('直播房间号为:' + roomid)
    else:
        print('抱歉,未找到此直播房间号~')
    while True:
        # 爬取:
        url = 'https://api.live.bilibili.com/ajax/msg'
        form = {
            'roomid': roomid,
            'visit_id': '',
            'csrf_token': token  # csrf_token就是cookie中的bili_jct字段;且有效期是7天!!!
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Cookie': cookie
        }
        html = requests.post(url, data=form)
        result = html.json()['data']['room']
        for i in result:
            print('[' + i['nickname'] + ']:' + i['text'])

        barrage = result[random.randint(0, len(result) - 1)]['text'] + '666'  # 随机取出第7,8,9条弹幕中的任一条来发送
        # 跟随发送:
        url_send = 'https://api.live.bilibili.com/msg/send'
        data = {
            'color': '16777215',
            'fontsize': '25',
            'mode': '1',
            'msg': barrage,
            'rnd': int(time.time()),
            'roomid': roomid,
            'csrf_token': token
        }
        try:
            html_send = requests.post(url_send, data=data, headers=headers)
            result = html_send.json()
            if result['msg'] == '你被禁言啦':
                print('*' * 30 + '您被禁言啦!!! 跟随弹幕发送失败~' + '*' * 30)
                exit()
            if result['code'] == 0 and result['msg'] == '':
                print('*' * 30 + '[' + barrage + ']' + ' 跟随弹幕发送成功~' + '*' * 30)
            else:
                print('*' * 30 + '[' + barrage + ']' + ' 跟随弹幕发送失败' + '*' * 30)
        except:
            print('*' * 30 + '[' + barrage + ']' + ' 跟随弹幕发送失败' + '*' * 30)
        time.sleep(1)


if __name__ == '__main__':
    main()
