from distutils.log import error
import subprocess
import time
import pickle
from datetime import datetime
from winreg import *


cooldown = False

def set_data(data):
    try:
        with open("times.pkl", "wb") as file:
            pickle.dump(data, file)
            return True
    except:
        return None


def get_data():
    try:
        with open("times.pkl", "rb") as data:
            return pickle.load(data)
    except:
        return None

def read_theme():
    personalize = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    path = HKEY_CURRENT_USER
    try:
        key = OpenKeyEx(path, personalize)
        value = QueryValueEx(key, "AppsUseLightTheme")
        if key:
            CloseKey(key)
        return value[0]
    except Exception as e:
        print(e)

    

def change_theme(theme):
    value = "0"
    if (theme == "Light"):
        value = "1"
    command = ['reg.exe', 'add', 'HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize', 
               '/v', f'AppsUseLightTheme', '/t', 'REG_DWORD', '/d', value, '/f']
    subprocess.run(command)

def check_times():
    times = get_data()
    day = datetime.strptime(times['day'], "%H:%M:%S").time()
    night = datetime.strptime(times['night'], "%H:%M:%S").time()
    current_time = datetime.strptime(datetime.strftime(datetime.now(), "%H:%M%S"), "%H:%M:%S").time()
    orders = ["Dark", "Light"] if day > night else ["Light", "Dark"]
    times = sorted([day, night, current_time])
    if (current_time == day):
        change_theme("Light")
    elif (current_time == night):
        change_theme("Dark")
    if ((current_time > day and current_time > night) or (current_time < day and current_time < night)):
        change_theme(orders[1])
    elif (times.index(current_time) == 1):
        change_theme(orders[0])


def listen():
    while (True):
        check_times()
        time.sleep(1)

def main():
    data = get_data()
    if (data == None):
        return
    listen()


if __name__ == '__main__':
    try:
        main()
    except error as err:
        with open("logs.txt", "wb") as file:
            file.write(err)


