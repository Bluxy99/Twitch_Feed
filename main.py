import os
import sys
import time
import traceback
from datetime import datetime

import requests
from colorama import Fore
from discordwebhook import Discord
from win10toast import ToastNotifier

#your webhook (leave blank to disable feed discord)
webhook = ""
#your twitch user id
myid = ""
#auth (https://dev.twitch.tv/docs/authentication)
clientId = ""
token = ""

nt = ToastNotifier()

def error(e):
    s = datetime.now()
    with open("./logs.txt", "w") as f:
        x = f.write(s.strftime("[%H:%M:%S]"+str(e)+"\n"))
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
    open("./logs.txt", "w")

def live():
    clear()
    print(f"        {Fore.RESET}[{Fore.LIGHTBLUE_EX}INFO{Fore.RESET}] {Fore.LIGHTBLACK_EX}Live check of you follow channel's is started! {Fore.RESET}(CTRL+C to STOP)")
    live = [] #channel live
    f = [] #self follow channel
    while True:
        time.sleep(4)
        #get follow channel (max 100)
        r = requests.get(f"https://api.twitch.tv/helix/users/follows?from_id={myid}&first=100", headers={"Client-ID": str(clientId), "Authorization": f"Bearer {token}"})
        if r.status_code == 200:
            i = r.json()
            for x in i["data"]:
                f.append(x["to_name"])
        for v in f:
            #check streams
            if v not in live:
                r = requests.get("https://api.twitch.tv/helix/streams?", params={"user_login": str(v)}, headers={"Client-ID": str(clientId), "Authorization": f"Bearer {token}"})
                if r.status_code == 200:
                    i = r.json()
                    for v1 in i["data"]:#live info
                        live.append(v)
                        os.system("title "+"Twitch_feed (Made by Bluxy99) - Channel Live: "+str(len(live))+"")
                        print(f"\n───────────────────────────────\n{Fore.RESET}[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Live\n"+Fore.LIGHTBLACK_EX+"Channel: "+Fore.RESET+str(v1["user_name"])+"\n"+Fore.LIGHTBLACK_EX+"Game: "+Fore.RESET+str(v1["game_name"]).upper()+Fore.RESET+"\n"+Fore.LIGHTBLACK_EX+"Title: "+Fore.RESET+str(v1["title"])+Fore.RESET+"\n───────────────────────────────\n")
                        if os.name == "nt":#win notify
                            nt.show_toast(str(v1["user_name"])+" is live!", str(v1["game_name"])+"\n"+str(v1["title"]))
                        if webhook.startswith("https://discord.com/api/webhooks/"):#discord notify
                            ds = Discord(url=f"{webhook}")
                            ds.post(content=""+str(v1["title"])+"\ntwitch.tv/"+str(v1["user_name"]).lower()+"\n")
            else:
                #check if channel is not longer live
                r = requests.get("https://api.twitch.tv/helix/streams?", params={"user_login": str(v)}, headers={"Client-ID": str(clientId), "Authorization": f"Bearer {token}"})
                if r.status_code == 200:
                    i = r.json()
                    if i["data"]:
                        continue
                    else:
                        live.remove(v)
                        os.system("title "+"Twitch_feed (Made by Bluxy99) - Channel Live: "+str(len(live))+"")
                        print(f"{Fore.RESET}[{Fore.LIGHTRED_EX}-{Fore.RESET}] {v} is now offline!")
                        if os.name == "nt":
                            nt.show_toast(v, "is now offline!")

if __name__ == "__main__":
    try:
        live()
    except KeyboardInterrupt:
        os.system("title "+"Twitch_feed (Made by Bluxy99)")
        clear()
        print(f"        {Fore.RESET}[{Fore.LIGHTBLUE_EX}!{Fore.RESET}] {Fore.LIGHTBLACK_EX}Bye!{Fore.RESET}")
        sys.exit(0)
    except Exception:
        clear()
        error(traceback.format_exc())