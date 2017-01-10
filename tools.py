# -*- coding:utf-8 -*-

from ctypes import *
from ctypes.wintypes import BOOL, UINT, LONG, LPCWSTR, HWND, WPARAM, LPARAM

import datetime
import time
import webbrowser

import urllib.request
import json

import codecs
import html.parser

HOUR = 5
MINUTE = 30
URL = ["http://weather.yahoo.co.jp/weather/jp/9/4110/9208.html",
        "http://www.e-typing.ne.jp/member/",
        "https://www.youtube.com/watch?v=qfsr0S_QGOU"]


WEATHERURL = "http://weather.livedoor.com/forecast/webservice/json/v1?city={}"


TVSCHEDULEURL = "http://tv.so-net.ne.jp/chart/23.action?head=%04d%02d%02d0000&span=24"

TVNUMLIST = {
        "101024":"NHK総合",
        "101032":"NHK教育",
        "101040":"日テレ ",
        "101064":"テレ朝 ",
        "101048":"TBS    ",
        "101072":"テレ東 ",
        "101056":"フジTV ",
        "123608":"       ",
        "101088":"       "
        }

TVKEYWORD = [
        "人工知能"
        ]


#####DEBUG######
DEBUG = True
if DEBUG:
    now = datetime.datetime.today()
    HOUR = now.hour
    MINUTE = now.minute + 1
######END#######


#----- line() -----#
def line():
    print('*' * 60)


#----- alarm() -----#
def alarm(hour, minute, url):
    while True:
        now = datetime.datetime.today()
        if now.hour == hour and now.minute == minute:
            for i in url:
                webbrowser.open(i)
            break

#----- getforecast -----#
def getforecast(location):
    print("===== 天気 =====")

    resp = urllib.request.urlopen(WEATHERURL.format(location)).read()
    resp = json.loads(resp)

    print("### {0} ###".format(resp['location']['city']))
    for forecast in resp['forecasts']:

        print("{0}\t({1})\t{2}".format(
            forecast['dateLabel'],
            forecast['date'],
            forecast['telop']), end='')

        for temper in forecast['temperature']:
            if forecast['temperature'][temper] != None:
                print("\t{}:{}C".format(
                    temper,
                    forecast['temperature'][temper]['celsius']), end='')
        print('')
    #line()
    #print(resp['description']['text'])
    #line()


#----- offdisplay -----#
def offdisplay():
    #user32 = windll.user32

    #user32.MessageBoxA(
    #        0,
    #        "Hello, MessageBox!",
    #        "Python to Windows API",
    #        0x00000040)

    user322 = windll.LoadLibrary('user32.dll')

    PostMessage = WINFUNCTYPE(BOOL, HWND, UINT, WPARAM, LPARAM)(
            ('PostMessageW', user322),
            ((1,'hwndParent'),
                (1,'hwndChildAfter'),
                (1,'lpClassName'),
                (1,'lpWindowName'),
                )
            )
    HWND_BROADCAST = 0xFFFF
    WM_SYSCOMMAND = 0x0112
    SC_MONITORPOWER = 0xF170
    DISPLAY_ON = -1
    DISPLAY_OFF = 2

    PostMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, DISPLAY_OFF)
    #time.sleep(1)
    #PostMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, DISPLAY_ON)


#===== TVParser() =====#
class TVParser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.title_flag = False
        self.data_results = []
        self.date_buff = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name,value in attrs:
                if name == "href" and "/schedule/" in value:
                    self.date_buff = value
                    self.date_buff = self.date_buff.replace("/schedule/", '')
                    self.date_buff = self.date_buff.replace(".action", '')

        if tag == "span":
            for name,value in attrs:
                if value == "schedule-title":
                    self.title_flag = True

    def handle_data(self, data):
        if self.title_flag:
            self.data_results.append((self.date_buff, data))
            self.title_flag = False



#----- gettvschedule() -----#
def gettvschedule():
    print("===== テレビ =====")

    now = datetime.datetime.today()
    tmrow = now + datetime.timedelta(days=1)
    date_list = [TVSCHEDULEURL % (now.year, now.month, now.day),
            TVSCHEDULEURL % (tmrow.year, tmrow.month, tmrow.day)]

    tvsearch_result = []

    for tvscheduleurl_date in date_list:

        response = urllib.request.urlopen(tvscheduleurl_date)
        page = response.read()

        page = page.decode('utf-8', 'ignore')

        page = page.replace("<wbr/>", ' ')
        page = page.replace("　", '  ')

        if DEBUG:
            fd = codecs.open("data.html", 'w+', 'utf-8')
            fd.write(page)
            fd.close()

        parser = TVParser()
        parser.feed(page)

        for tvshow in parser.data_results:
            tvprogram = [TVNUMLIST[tvshow[0][0:6]],
                    "{0}/{1}/{2}".format(
                        tvshow[0][6:10],
                        tvshow[0][10:12],
                        tvshow[0][12:14]),
                    "{0}:{1}".format(
                        tvshow[0][14:16],
                        tvshow[0][16:18]),
                    tvshow[1]
                    ]

            #print(tvprogram)

            for key in TVKEYWORD:
                if key in tvprogram[3]:
                    tvsearch_result.append(tvprogram)

        for tv in tvsearch_result:
            print(tv)



#----- displayoff() -----#
def displayoff():
    print("{}:{}:00 (now {})".format(HOUR, MINUTE, datetime.datetime.today()))
    time.sleep(5)
    offdisplay()


#----- main() -----#
def main():
    displayoff()
    alarm(HOUR, MINUTE, URL)
    getforecast("090010")
    gettvschedule()
    input()

#----- __name__ -----#
if __name__ == "__main__":
    main()
