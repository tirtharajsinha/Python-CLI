import time
import subprocess
import argparse
import requests
from sys import platform

TGREEN = '\033[32m'
TRED = '\033[31;2m'
TCYAN = '\033[36;2m'
TPURPLE = '\033[35m'
TYELLOW = '\033[33m'
TBLUE = '\033[34;1m'
ENDC = '\033[m'  # reset to the defaults

time.sleep(1)
microsoft = "" \
            "                           __" \
            "\n                       ,-~¨^  ^¨-,           _," \
            "\n                      //////////// ;^-._...,¨/" \
            "\n                     //////////// ///////////" \
            "\n                    //////////// ///////////" \
            "\n                   //////////// ///////////" \
            "\n                  /,.-:''-,_ / ///////////" \
            "\n                  _,.-:--._ ^ ^:-._ __../" \
            "\n                //////////// /¨:.._¨__.;" \
            "\n               //////////// ///////////" \
            "\n              //////////// ///////////" \
            "\n             //////////// ///////////" \
            "\n            /_,.--:^-._/ ///////////" \
            "\n           ^            ^¨¨-.___.:^               "


# traverse the info
class WinSystem:
    def __init__(self):
        Id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
        Id = Id[1:-1]
        new = []

        # arrange the string into clear info
        for item in Id:
            pair = item.split("\r")[:-1][0]
            new.append(pair)
        # for i in range(len(new)):
        #     print(i, new[i])
        self.info = new
        self.ignore = []

    def sysinfo(self):
        if "Windows" in self.info[1]:
            print(TCYAN + microsoft + ENDC)
        self.ignore = [4, 5, 7, 8, 9, 10, 11, 16, 17, 18, 19, 21, 25, 26, 27]
        for i in range(27):
            if i not in self.ignore:
                data = self.info[i].split(":", 1)
                print(TBLUE + data[0] + " : " + TGREEN + data[-1] + ENDC)
                time.sleep(.3)

    def sysinfo_extra(self):
        addmore = [25, 26, 27]
        self.sysinfo()
        for i in range(25, len(self.info)):
            if i in addmore:
                data = self.info[i].split(":", 1)
                print(TPURPLE + data[0] + " : " + TYELLOW + data[-1] + ENDC)
                time.sleep(.3)

        netindex = -1
        for i in range(30, len(self.info)):
            title = self.info[i].split(":")
            if "Network Card(s)" in title[0]:
                netindex = i
                break

        if netindex != -1:
            for i in range(netindex, netindex + 8):
                data = self.info[i].split(":", 1)
                if len(data) != 1:
                    print(TCYAN + data[0].strip() + " : " + ENDC + data[-1])
                else:
                    print(TCYAN + data[0].strip() + ENDC)
                time.sleep(.3)


class Weather:
    def __init__(self):
        self.baseurl = "http://api.openweathermap.org/data/2.5/weather?q="
        self.weatherapi = "8e44efb0ae84f237a5d93f5f4d629433"

    def fetchweather(self):
        place = input("Enter location : ")
        url = self.baseurl + place + "&appid=" + str(self.weatherapi) + "&units=metric"
        res = requests.get(url)
        data = res.json()
        if data["cod"] == 200:
            print(TYELLOW + "city found" + ENDC)
            print("------------------------\n")

            city = data["name"]
            country = data["sys"]["country"]
            windspeed = data["wind"]["speed"]
            pressure = data["main"]["pressure"]
            temp = data["main"]["temp"]
            hum = data["main"]["humidity"]
            visi = data["visibility"]
            des = data["weather"][0]["description"]
            time.sleep(.5)
            print(TPURPLE + "city : " + ENDC + str(city) + "," + str(country))
            time.sleep(.5)
            print(TPURPLE + "Temperature : " + ENDC + str(temp), "degree celcius")
            time.sleep(.5)
            print(TPURPLE + "Humidity : " + ENDC + str(hum), "%")
            time.sleep(.5)
            print(TPURPLE + "Visibility : " + ENDC + str(visi), "meteres")
            time.sleep(.5)
            print(TPURPLE + "Wind speed : " + ENDC + str(windspeed), "miles/h")
            time.sleep(.5)
            print(TPURPLE + "Pressure : " + ENDC + str(pressure), "hPa")
            time.sleep(.5)
            print(TYELLOW + "Overall : " + ENDC + str(des))
            print("\n......... Data from https://openweathermap.org/\n")


def recognize_os(e=False):
    if platform == "linux" or platform == "linux2":
        print("sorry currently this feature doesn't effective on any other system than Windows")
    elif platform == "darwin":
        print("sorry currently this feature doesn't effective on any other system than Windows")
    elif platform == "win32":
        if e:
           WinSystem().sysinfo_extra()
        else:
            WinSystem().sysinfo()


# Windows...

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--system", action="store_true", help="find your system info")
    parser.add_argument("-e", "--extra", action="store_true", help="find extra system info")
    parser.add_argument("-w", "--weather", action="store_true", help="Fetch weather report")
    args = parser.parse_args()
    if args.system:
        recognize_os()
    elif args.extra:
        recognize_os(e=True)
    elif args.weather:
        Weather().fetchweather()
    else:
        print("No instruction found,\nTry 'cli.exe -h' for more info.")
