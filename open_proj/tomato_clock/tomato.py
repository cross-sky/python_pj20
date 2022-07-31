'''
Author: sherry
LastEditors: error: git config user.name & please set dead value or install git
Date: 2022-07-24 11:01:45
FilePath: \open_project\tomato_clock\tomato.py
Description: 
Copyright (c) 2022 by sherry , All Rights Reserved.
'''
from logging import exception
import sys
import time
import subprocess
from winotify import Notification, audio

WORK_MINUTES = 5
BREAK_MINUTES = 5
WORK_STRING = 'It is time to take a break.'
BREAK_STRING = 'It is time to take a work.'

def main():
    try:
        if len(sys.argv) <= 1:
            work_print(WORK_MINUTES)
            tomato(WORK_MINUTES, WORK_STRING)
            break_print(BREAK_MINUTES)
            tomato(BREAK_MINUTES, BREAK_STRING)
        elif sys.argv[1] == '-t':
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else WORK_MINUTES
            work_print(minutes)
            tomato(minutes, WORK_STRING)
        elif sys.argv[1] == '-b':
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else BREAK_MINUTES
            break_print(minutes)
            tomato(minutes, BREAK_STRING)
        elif sys.argv[1] == '-h':
            help()
        else:
            help()
    except KeyboardInterrupt:
        print('\n 👋 goodbye ')
    except Exception as e:
        print(e)
        exit(1)


def work_print(minutes):
    print(f"🍅 tomato {minutes} minutes. Ctrl+c to exit")

def break_print(minutes):
    print(f"🛀 break {minutes} minutes. Ctrl+c to exit")

def tomato(minutes, notify_msg):
    start_time = time.perf_counter()
    while True:
        diff_seconds = int(round(time.perf_counter()) - start_time)
        left_seconds = minutes*60 - diff_seconds
        if left_seconds <= 0:
            print('')
            break

        countdown = '{}:{} ⏰'.format(int(left_seconds/60), int(left_seconds%60))
        duration = min(minutes, 25)
        processbar(diff_seconds, minutes*60, duration, countdown)
        time.sleep(1)
    notify_me(notify_msg)

def help():
    pass

def processbar(curr, total, duration=10, extra=''):
    frac = curr / total
    filled = round(frac * duration)
    print('\r', '🍅' * filled + '--' * (duration - filled), '[{:.0%}]'.format(frac), extra, end='')

def notify_me(notify_msg):
    print(notify_msg)
    toast = Notification(app_id='tomato clock🍅',
                        title="tomoto clock",
                        msg=notify_msg,
                        icon='tea.ico')
    toast.set_audio(audio.SMS, loop=False)
    toast.show()

if __name__ == '__main__':
    main()


