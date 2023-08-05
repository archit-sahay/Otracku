#!/usr/bin/python -tt

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import os
import discord
import time
from datetime import datetime
from pytz import timezone
from dotenv import load_dotenv
from discord.ui import Select,View
from discord.ext import commands
import asyncio
from AnilistPython import Anilist
anilist=Anilist()
load_dotenv()

def tff(t):
        if t[-2:] == "AM" and t[:2] == "12":
                return tftn("00" + t[2:-2])
        elif t[-2:] == "AM":
                return tftn(t[:-2])
        elif t[-2:] == "PM" and t[:2] == "12":
                return tftn(t[:-2])
        else:
                return tftn(str(int(t[:2]) + 12) + t[2:6])

def tftn(tf):
        return int(tf[:2])*100+int(tf[3:])


TOKEN = os.getenv('MTAzNDQzODkzODk1OTU0NDMyMg.G__-4I.gy7u310oWnTI34fv_amSkOlV_ye_eNfwVwCPMw')
intents = discord.Intents()
intents.emojis = True
intents.messages = True
intents.presences = True
intents.message_content = True
client = commands.Bot(command_prefix=".",intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching,
        name='you guys waste your time on Anime and Manga'))
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)

@client.command()
async def info(ctx):
    help=discord.Embed(title='Instruction Manual for Otracku', description='List of commands you can use and what they are for.')
    help.add_field(name="info",value='Gives a list of all commands',inline=False)
    help.add_field(name='setr',value='Sets a reminder for all the episodes of the show given as parameter until it stops airing. Different Seasons are treated as different shows. Do no give spaces between the words of name of the show',inline=False)
    help.add_field(name='anisyn',value="Gives Synopsis of an anime. That's pretty much it",inline=False)
    help.add_field(name='mansyn',value='Gives Synopsis of a manga.',inline=False)
    help.set_thumbnail(url=client.user.avatar)
    await ctx.send(embed=help)

@client.command()
async def setr(ctx,*,ded):
    url="https://animeschedule.net"
    chrome_driver_path="C:\Program Files (x86)\chromedriver.exe"
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    service=Service(executable_path=chrome_driver_path)
    driver=webdriver.Chrome(service=service,options=options)
    driver.get(url)
    today=driver.find_elements(By.ID, "active-day")
    lol=driver.find_elements(By.CSS_SELECTOR, "a .show-title-bar")
    anime=today[0].find_elements(By.CSS_SELECTOR, "a .show-title-bar")
    tme=today[0].find_elements(By.CSS_SELECTOR, "h3 .show-air-time")
    ts={}
    all=[]
    for uf in lol:
        all.append(str(uf.text))
    for x in range(len(tme)):
        if str(anime[x].text) != "":
            ts[str(anime[x].text)]=str(tme[x].text)

    driver.quit()
    print(ts)
    if ded in all:
        await ctx.send(f'Reminder is set for {ded}')
        while(ded in all):
            if ded in ts.keys():
                india=timezone('Asia/Kolkata')
                tx=(datetime.now(india))
                txu=datetime.now()
                tn=tftn(tx.strftime('%H:%M'))
                # print(tff(ts[ded])<=tn)
                if tff(ts[ded])>tn:
                    # print("aired")
                    # await ctx.send(f'{ctx.author.mention} {ded} has a new Episode')
                    at=datetime.strptime(ts[ded],'%I:%M %p')
                    # tx.replace(tzinfo=None)
                    uff=at - txu
                    ok=uff.total_seconds()
                    await asyncio.sleep(int(ok))
                await ctx.send(f'{ctx.author.mention} {ded} has a new Episode')
                await asyncio.sleep(604800)
            else:
                await asyncio.sleep(86400)
            options=webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            service=Service(executable_path=chrome_driver_path)
            driver=webdriver.Chrome(service=service,options=options)
            driver.get(url)
            today=driver.find_elements(By.ID, "active-day")
            lol=driver.find_elements(By.CSS_SELECTOR, "a .show-title-bar")
            anime=today[0].find_elements(By.CSS_SELECTOR, "a .show-title-bar")
            tme=today[0].find_elements(By.CSS_SELECTOR, "h3 .show-air-time")
            ts={}
            all=[]
            for uf in lol:
                all.append(str(uf.text))
            for x in range(len(tme)):
                if str(anime[x].text) != "":
                    ts[str(anime[x].text)]=str(tme[x].text)
            driver.quit()
        await ctx.send(f'{ded} has ended. See you next when the next season airs')
    else:
        await ctx.send(f'{ded} is not airing as of now')
        # print(set(all)
    # a=anilist.get_anime(ded)
    # while(a['airing_status']=='RELEASING'):
    #     ok=a['next_airing_ep']['timeUntilAiring']
    #     await ctx.send(f'Reminder in {ok} seconds (Please do the Math yourself)')
    #     await asyncio.sleep(ok)
        # await ctx.send(f'{ctx.author.mention} {ded} has a new Episode')
    #     a=anilist.get_anime(ded)
    # await ctx.send(f'{ded} has ended. See you next when the next season airs')

@client.command()
async def anisyn(ctx,ded=""):
    a=anilist.get_anime(ded)
    n=a['name_romaji']
    d=a['desc']
    syn=discord.Embed(title=f'{n}',description=f'{d}')
    syn.set_thumbnail(url=a['cover_image'])
    await ctx.send(embed=syn)

@client.command()
async def mansyn(ctx,ded=""):
    a=anilist.get_manga(ded)
    n=a['name_romaji']
    d=a['desc']
    syn=discord.Embed(title=f'{n}',description=f'{d}')
    syn.set_thumbnail(url=a['cover_image'])
    await ctx.send(embed=syn)

client.run('MTAzNDQzODkzODk1OTU0NDMyMg.G__-4I.gy7u310oWnTI34fv_amSkOlV_ye_eNfwVwCPMw')
