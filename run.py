import time
import pickle 
import os
import getpass
import subprocess
from win32com.client import Dispatch

commands = ["start", "stop", "set", "set times", "view", "view times", "menu", "close"]
executes = {}
USER_NAME = getpass.getuser()


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

def clear_screen():
    os.system('cls')

def validate_times(day, night):
    if (":" not in day or ":" not in night):
        return False

    day_list = day.split(":")
    night_list = night.split(":")
    day_result = False
    night_result = False
    for num in day_list:
        if (1 <= len(num) <= 2 and num.isalnum()):
            day_result = True

    for num in night_list:
        if (1 <= len(num) <= 2 and num.isalnum()):
            night_result = True
    
    return day_result and night_result

def format_times(day, night):
    day_result = []
    night_result = []
    for time in day.split(":"):
        day_result.append("{:02d}".format(int(time)))
    day_result.append("00")
    
    for time in night.split(":"):
        night_result.append("{:02d}".format(int(time)))
    night_result.append("00")
    
    return [':'.join(day_result), ':'.join(night_result)]


        

def set_times():
    clear_screen()
    print("Enter inputs in 24 hour format (HH:mm)")
    print("Type menu to go menu")
    day = input("Input day time: ").lower()
    if (day == "menu"):
        command_handler(day)
    night = input("Input night time: ").lower()
    if (night == "menu"):
        command_handler(night)
    validate = validate_times(day, night)
    if (validate):
        day, night = format_times(day, night)
        data = {"day": day, "night": night}
        status = set_data(data)
        if (status):
            print("Succesfully added")
        else:
            print("Failed")
            time.sleep(3)
            set_times()

        print("\nMenu - View Times - Close")
        option = input("Input: ").lower()
        status = command_handler(option)
        if (status == -1):
            set_times()
    else:
        print("Input format is incorrent.")
        time.sleep(2)
        set_times()
        


def view_times():
    clear_screen()
    times = get_data()
    if (times != None):
        print(f"Day: {times['day']}\nNight: {times['night']}")
    else: 
        print("Data is not found. Try creating one")

    print("\nSet Times - Menu - Close")
    option = input("Input: ").lower()
    status = command_handler(option)
    if (status == -1):
        view_times()

def command_handler(cmd):
    if (cmd in commands):    
        cmd = cmd.split()[0]
        executes[cmd]()
    else:
        print("Command not found!")
        time.sleep(2)
        return -1

def toggle_start():
    times = get_data()
    if (times):
        return True
    else:
        return None

def start():
    is_running = process_exists("themelistener.exe")
    if (not is_running):
        status = toggle_start()
        if (status):
            os.system("start themelistener.exe")
        else:
            print("Data not found.")
            time.sleep(2)
    main()

def stop():
    toggle_start()
    os.system("TASKKILL /F /IM themelistener.exe")
    time.sleep(2)
    main()

def exit():
    os.system("exit")

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

def main():
    clear_screen()
    is_start = process_exists("themelistener.exe")
    print("Windows Theme Changer Timer by indiff")
    print(f"Status: {'ON' if is_start else 'OFF'}")
    print("\nList of commands:")
    print(f"{'Stop' if is_start else 'Start'} - Set Times - View Times - Close")
    
    option = input("\nInput: ").lower()
    status = command_handler(option)
    if (status == -1):
        main()




if __name__ == '__main__':
    executes = {"set":set_times, "view":view_times, "close":exit, "menu":main, "start":start, "stop":stop}
    main()
    