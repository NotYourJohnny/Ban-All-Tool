import os
import sys
import time
import requests
import json
import discord
import asyncio
import threading
from discord.ext import commands
import colorama
from colorama import Fore

with open('config.json') as f:
    config = json.load(f)
token = config.get('bottoken')

intents = discord.Intents.all()
intents.members = True

headers = {'Authorization': f'Bot {token}'}
client = commands.Bot(command_prefix=".", case_insensitive=False, intents=intents)
client.remove_command("help")

i = 0
membercount = 0

@client.event
async def on_ready():
    await guild()

async def menuban():
    os.system('cls & mode 70, 40')
    guild = guildid
    txt = open('core/botscrape.txt')
    for member in txt:
        threading.Thread(target=massban, args=(guild, member,)).start()
    txt.close()
    time.sleep(4)

def massban(guild, member):
    global i, membercount
    while True:
        r = requests.put(f"https://discord.com/api/v8/guilds/{guild}/bans/{member}", headers=headers)
        if 'retry_after' in r.text:
            time.sleep(r.json()['retry_after'])
        else:
            if r.status_code == 200 or r.status_code == 201 or r.status_code == 204:
                while i < membercount:
                    i+=1
                    if i == 1:
                        print(f" [{Fore.RED}>{Fore.RESET}] %dst user has been banned"%(i))
                    elif i == 2:
                        print(f" [{Fore.RED}>{Fore.RESET}] %dnd user has been banned"%(i))
                    elif i == 3:
                        print(f" [{Fore.RED}>{Fore.RESET}] %drd user has been banned"%(i))
                    else:
                        print(f" [{Fore.RED}>{Fore.RESET}] %dth user has been banned"%(i))
                break
            else:
                break

async def main():
    if len(sys.argv) < 2:
        os.system('cls & mode 70, 12')
        sys.stdout.write(f'''
    
    [{Fore.RED}>{Fore.RESET}] Connected as: {client.user} [BOT]
    [{Fore.RED}>{Fore.RESET}] Guild: {guildid}

    ''')

    option = input(f"[{Fore.RED}>{Fore.RESET}] Mass ban [y{Fore.RED}/{Fore.RESET}n]: ")
    if option == 'y':
        await menuban()
        await guild()
    if option == 'n':
        await guild()
    else:
        print(f''' 
 [{Fore.RED}>{Fore.RESET}] Invalid option''')
        time.sleep(0.5)
        main()

async def guild():
    global membercount, guildid
    os.system('cls & mode 70, 12')
    guildid = int(input(f''' 
 [{Fore.RED}>{Fore.RESET}] Guild ID: '''))
    await client.wait_until_ready()
    ob = client.get_guild(guildid)
    members = await ob.chunk()
    os.remove("core/botscrape.txt")

    with open('core/botscrape.txt', 'a') as txt:
        for member in members:
            txt.write(str(member.id) + "\n")
            membercount += 1
        if membercount == 1:
            print(f''' 
 [{Fore.RED}>{Fore.RESET}] Successfully scraped {Fore.RED}{membercount}{Fore.RESET} members''')
        else:
            print(f''' 
 [{Fore.RED}>{Fore.RESET}] Successfully Scraped {Fore.RED}{membercount}{Fore.RESET} members''')
        txt.close()
        time.sleep(1)
        await main()

def check():
    os.system('cls & mode 70, 12 & title discord mass ban │ by lxw edited by lyk')
    try:
        client.run(token)
    except:
        print(f'''
 [{Fore.RED}>{Fore.RESET}] Invalid Token''')
        time.sleep(2)

check()