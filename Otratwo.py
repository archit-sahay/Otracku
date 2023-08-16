
import os
import discord
import time
import asyncio
from datetime import datetime
from pytz import timezone
from dotenv import load_dotenv
from discord.ui import Select,View
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
load_dotenv()

#The function tff takes a string in 12 hour format and converts into 24 hour format string
#10:30 PM to 22:30 in string format
def tff(t):
        if t[-2:] == "AM" and t[:2] == "12":
                return tftn("00" + t[2:-2])
        elif t[-2:] == "AM":
                return tftn(t[:-2])
        elif t[-2:] == "PM" and t[:2] == "12":
                return tftn(t[:-2])
        else:
                return tftn(str(int(t[:2]) + 12) + t[2:6])

#The function tftn converts 24 hour format string to integer
#'22:30' to 2230
def tftn(tf):
        return int(tf[:2])*100+int(tf[3:])

#PaginationView is a class for displaying multple search results for the query in different pages using embeds and buttons
class PaginationView(discord.ui.View):
    curp:int=0
    async def send(self,ctx):
        self.message=await ctx.send(view=self)
        await self.update_message(self.data[0])

    async def update_message(self,data):
        self.update_buttons()
        await self.message.edit(embed=data,view=self)

    def update_buttons(self):
        if self.curp==0:
            self.first_button.disabled=True
            self.prev_button.disabled=True
        else:
            self.first_button.disabled=False
            self.prev_button.disabled=False

        if self.curp==len(self.data)-1:
            self.last_button.disabled=True
            self.next_button.disabled=True
        else:
            self.last_button.disabled=False
            self.next_button.disabled=False

    @discord.ui.button(label="First",style=discord.ButtonStyle.primary)
    async def first_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.curp=0
        await self.update_message(self.data[self.curp])

    @discord.ui.button(label="Previous",style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.curp-=1
        await self.update_message(self.data[self.curp])

    @discord.ui.button(label="Next",style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.curp+=1
        await self.update_message(self.data[self.curp])

    @discord.ui.button(label="Last",style=discord.ButtonStyle.primary)
    async def last_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.curp=len(self.data)-1
        await self.update_message(self.data[self.curp])

TOKEN = os.getenv(token)
intents = discord.Intents()
intents.emojis = True
intents.messages = True
intents.presences = True
intents.message_content = True
client = commands.Bot(command_prefix=".",intents=intents)

#On_ready basically determines the status message when bot starts or goes online
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching,
        name='you guys waste your time on Anime and Manga'))
    print(f'{client.user} has connected to Discord!')

#On_message prevents the bot from treating it's own messages as commands and also looks in all messages for commands
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)

#Info command is just as the name suggests, a command to get info on what commands one can use with the bot
@client.command()
async def info(ctx):
    help=discord.Embed(title='Instruction Manual for Otracku', description='List of commands you can use and what they are for.')
    help.add_field(name="info",value='Gives a list of all commands',inline=False)
    help.add_field(name='setr',value='Sets a reminder for all the episodes of the show given as parameter until it stops airing. Different Seasons are treated as different shows. Do no give spaces between the words of name of the show',inline=False)
    help.add_field(name='anisyn',value="Gives Synopsis of an anime. That's pretty much it",inline=False)
    help.add_field(name='mansyn',value='Gives Synopsis of a manga.',inline=False)
    help.set_thumbnail(url=client.user.avatar)
    await ctx.send(embed=help)

#Setr is a command for setting reminder for any airing show
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

#Anisyn is a command to search for any anime and get their synopsis
#It scrapes all the search results from the site and displays them using the PaginationView class defined above
@client.command()
async def anisyn(ctx,*,ded):
    url=f'https://anilist.co/search/anime?search={ded}'
    chrome_driver_path="C:\Program Files (x86)\chromedriver.exe"

    options=webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")
    service=Service(executable_path=chrome_driver_path)
    driver=webdriver.Chrome(service=service)#,options=options)

    driver.get(url)
    time.sleep(7)
    but=driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div/div[4]/div[2]/div[2]/div[2]')
    but.click()
    anime=driver.find_elements(By.CLASS_NAME, "description")
    links=driver.find_elements(By.CSS_SELECTOR,"img.image")
    title=driver.find_elements(By.CLASS_NAME, "title")
    embeds=[]
    desc=[]
    imgs=[]
    titl=[]
    for ded in anime:
    	desc.append(str(ded.text))
    for x in links:
    	imgs.append(str(x.get_attribute('src')))
    for x in title:
    	titl.append(str(x.text))
    for x in range(len(links)):
        uf=discord.Embed(title=titl[x],description=desc[x])
        uf.set_thumbnail(url=imgs[x])
        embeds.append(uf)
    driver.quit()
    pv=PaginationView()
    pv.data=embeds
    await pv.send(ctx)

#Mansyn is a command to search for any anime and get their synopsis
#It works similarly to Anisyn command just scrapes a different site for results
@client.command()
async def mansyn(ctx,*,ded):
    url=f'https://anilist.co/search/manga?search={ded}'
    chrome_driver_path="C:\Program Files (x86)\chromedriver.exe"

    options=webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")
    service=Service(executable_path=chrome_driver_path)
    driver=webdriver.Chrome(service=service)#,options=options)

    driver.get(url)
    time.sleep(7)
    but=driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div/div[4]/div[2]/div[2]/div[2]')
    but.click()
    anime=driver.find_elements(By.CLASS_NAME, "description")
    links=driver.find_elements(By.CSS_SELECTOR,"img.image")
    title=driver.find_elements(By.CLASS_NAME, "title")
    embeds=[]
    desc=[]
    imgs=[]
    titl=[]
    for ded in anime:
    	desc.append(str(ded.text))
    for x in links:
    	imgs.append(str(x.get_attribute('src')))
    for x in title:
    	titl.append(str(x.text))
    for x in range(len(links)):
        uf=discord.Embed(title=titl[x],description=desc[x])
        uf.set_thumbnail(url=imgs[x])
        embeds.append(uf)
    driver.quit()
    pv=PaginationView()
    pv.data=embeds
    await pv.send(ctx)

client.run(token)
