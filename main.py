import json
import os
import socket
import sys
import time
import traceback
from datetime import datetime

import requests
import urllib3
#from bs4 import BeautifulSoup as bs
from colorama import Fore
from discordwebhook import Discord
from PyQt5 import QtCore, QtGui, QtWidgets
from win10toast import ToastNotifier

#your webhook (leave blank to disable feed discord)
webhook = ""
#your twitch user id (https://extpose.com/ext/8734)
myid = "415027694"
#auth (https://dev.twitch.tv/docs/authentication)
clientId = ""
token = ""
nt = ToastNotifier()
wsp = ""#leave blank
sps = wsp.center(24)

def error(e):
    t = datetime.now().strftime("[%H:%M:%S]"+str(e)+"\n")
    with open("./logs.txt", "w") as f:
        x = f.write(t+str(e))
    print("[!] Error!\n"+str(traceback.format_exc()))

def clear():
    os.system("cls" if os.name == "nt" else "echo -e \\\\033c")
    os.system("mode con: cols=105 lines=30")
    print(f"""{Fore.RESET}
                        {Fore.MAGENTA}┌┬┐┬ ┬┬┌┬┐┌─┐┬ ┬   ┌─┐┌─┐┌─┐┌┬┐
                        {Fore.LIGHTBLACK_EX} │ ││││ │ │  ├─┤───├┤ ├┤ ├┤  ││
                        {Fore.MAGENTA} ┴ └┴┘┴ ┴ └─┘┴ ┴   └  └─┘└─┘─┴┘
    """+Fore.RESET)

os.system("title "+"Twitch_feed (Made by Bluxy99)")
print(f"""{Fore.RESET}
                    {Fore.MAGENTA}┌┬┐┬ ┬┬┌┬┐┌─┐┬ ┬   ┌─┐┌─┐┌─┐┌┬┐
                    {Fore.LIGHTBLACK_EX} │ ││││ │ │  ├─┤───├┤ ├┤ ├┤  ││
                    {Fore.MAGENTA} ┴ └┴┘┴ ┴ └─┘┴ ┴   └  └─┘└─┘─┴┘
"""+Fore.RESET)
if not os.path.isfile("./logs.txt"):
    open("./logs.txt", "w", encoding="utf-8")
    open("./temp.json", "w", encoding="utf-8")

def gui():
    clear()
    try:
        op = input(f"{Fore.RESET}[{Fore.YELLOW}INFO{Fore.RESET}]{Fore.RESET} Select option: \n\n1|Start live check\n2|Exit\n")
        if op == "1":
            clear()
            live()
        if op == "2":
            clear()
            print(f"        {Fore.RESET}[{Fore.LIGHTBLUE_EX}!{Fore.RESET}] {Fore.LIGHTBLACK_EX}Bye!{Fore.RESET}")
            sys.exit(0)
        else:
            clear()
            print(f"{Fore.RESET}[{Fore.YELLOW}INFO{Fore.RESET}]{Fore.RESET} Select option...")
            gui()
    except ValueError:
        gui()
    except UnboundLocalError:
        gui()
    except Exception:
        clear()
        error(traceback.format_exc())

def live():
    clear()
    print(f"        {Fore.RESET}[{Fore.LIGHTBLUE_EX}INFO{Fore.RESET}] {Fore.LIGHTBLACK_EX}Live check of you follow channel's is started! {Fore.RESET}(CTRL+C to STOP)")
    live = [] #LIVE
    f = [] #follow channel
    try:
        while True:
            #get follow channel (max 100)
            r = requests.get(f"https://api.twitch.tv/helix/users/follows?from_id={myid}&first=100", timeout=30, headers={"Client-ID": str(clientId), "Authorization": f"Bearer {token}"})
            if r.status_code == 200:
                i = r.json()
                for x in i["data"]:
                    f.append(x["to_name"])
            for v in f:
                #check streams
                if v not in live:
                    r = requests.get(f"https://api.twitch.tv/helix/streams?user_login={v}", timeout=30, headers={"Client-ID": str(clientId), "Authorization": f"Bearer {token}"})
                    if r.status_code == 200:
                        t = datetime.now().strftime("%H:%M:%S")
                        i = r.json()
                        for v1 in i["data"]:#live info
                            live.append(v)
                            os.system("title "+"Twitch_feed (Made by Bluxy99) - Channel Live: "+str(len(live))+"")
                            print(f"\n{sps}───────────────────────────────\n{sps}{Fore.RESET}[{Fore.LIGHTGREEN_EX}LIVE{Fore.RESET}]|{t}\n{sps}"+Fore.LIGHTBLACK_EX+"Channel: "+Fore.RESET+str(v1["user_name"])+f"\n{sps}"+Fore.LIGHTBLACK_EX+"Game: "+Fore.RESET+str(v1["game_name"]).upper()+Fore.RESET+f"\n{sps}"+Fore.LIGHTBLACK_EX+"Title: "+Fore.RESET+str(v1["title"])+Fore.RESET+f"\n{sps}───────────────────────────────\n{sps}> Channel live: "+Fore.LIGHTBLACK_EX+str(len(live))+Fore.RESET+"\n")
                            if os.name == "nt":#win notify
                                nt.show_toast(str(v1["user_name"])+" is live!", str(v1["game_name"])+"\n"+str(v1["title"]))
                            if webhook.startswith("https://discord.com/api/webhooks/"):#discord notify
                                ds = Discord(url=f"{webhook}")
                                ds.post(content=""+str(v1["title"])+"\nhttps://www.twitch.tv/"+str(v1["user_name"]).lower()+"\n")
                else:
                    #check if channel is not longer live
                    r = requests.get(f"https://api.twitch.tv/helix/streams?user_login={v}", timeout=30,  headers={"Client-ID": str(clientId), "Authorization": f"Bearer {token}"})
                    if r.status_code == 200:
                        i = r.json()
                        if i["data"]:
                            continue
                        else:
                            t = datetime.now().strftime("%H:%M:%S")
                            live.remove(v)
                            os.system("title "+"Twitch_feed (Made by Bluxy99) - Channel Live: "+str(len(live))+"")
                            print(f"\n{sps}───────────────────────────────\n{sps}{Fore.RESET}[{Fore.LIGHTRED_EX}OFF-LIVE{Fore.RESET}]|{t}\n{sps}"+Fore.LIGHTBLACK_EX+"Channel: "+Fore.RESET+str(v)+Fore.RESET+f"\n{sps}───────────────────────────────\n{sps}> Channel live: "+Fore.LIGHTBLACK_EX+str(len(live))+Fore.RESET+"\n")
                            if os.name == "nt":
                                nt.show_toast(v, "is now offline!")
            time.sleep(300)
    except urllib3.exceptions.ReadTimeoutError:
        pass
    except socket.timeout:
        pass
    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.ConnectTimeout:
        pass
    except KeyboardInterrupt:
        os.system("title "+"Twitch_feed (Made by Bluxy99)")
        clear()
        gui()
    except Exception:
        clear()
        error(traceback.format_exc())

if __name__ == "__main__":
    try:
        gui()
    except KeyboardInterrupt:
        clear()
        print(f"        {Fore.RESET}[{Fore.LIGHTBLUE_EX}!{Fore.RESET}] {Fore.LIGHTBLACK_EX}Bye!{Fore.RESET}")
        sys.exit(0)
    except Exception:
        clear()
        error(traceback.format_exc())
