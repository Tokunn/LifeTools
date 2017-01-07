from ctypes import *
from ctypes.wintypes import BOOL, UINT, LONG, LPCWSTR, HWND, WPARAM, LPARAM

import datetime
import time
import webbrowser

import urllib.request
import json


HOUR = 5
MINUTE = 30
URL = "https://www.youtube.com/watch?v=qfsr0S_QGOU"


#####DEBUG######
DEBUG = True
if DEBUG:
    now = datetime.datetime.today()
    HOUR = now.hour
    MINUTE = now.minute + 1
######END#######

def line():
    print('*' * 60)

def alarm(hour, minute, url):
    while True:
        now = datetime.datetime.today()
        if now.hour == hour and now.minute == minute:
            webbrowser.open(url)
            break

def getforecast(location):
    resp = urllib.request.urlopen("http://weather.livedoor.com/forecast/webservice/json/v1?city={}".format(location)).read()
    resp = json.loads(resp)

    print(resp['location']['city'])
    for forecast in resp['forecasts']:
        print(forecast['dateLabel']+'\t('+forecast['date']+')\t'+forecast['telop'], end='')
        for temper in forecast['temperature']:
            if forecast['temperature'][temper] != None:
                print("\t{}:{}C".format(temper, forecast['temperature'][temper]['celsius']), end='')
        print('')
    line()
    print(resp['description']['text'])
    line()


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

def displayoff():
    print("{}:{}:00 (now {})".format(HOUR, MINUTE, datetime.datetime.today()))
    time.sleep(5)
    offdisplay()



def main():
    displayoff()
    alarm(HOUR, MINUTE, URL)
    getforecast("090010")
    input()

if __name__ == "__main__":
    main()
