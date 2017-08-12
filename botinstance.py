"""
Author: Sturza Mihai
GitHub: https://github.com/MArtzDEV

"""

import discord, urllib.request,asyncio, sys, time
from discord.ext import commands
from bs4 import BeautifulSoup
from termcolor import colored

# creates the bot instance
bot = commands.Bot("<>")

# prints some info about the bot after loggin in on the discord servers
@bot.event
@asyncio.coroutine
def on_ready():
    print("Commands will be displayed with",colored('blue','blue'),"errors with",colored('red','red'),"and bot the bot status with",colored('green','green'))
    print(colored("[LOGIN]","green"),"Logged in as {}".format(bot.user.name))

# this commands gets the firt paragraph of a webpage, displaying it for the user
@bot.command()
@asyncio.coroutine
async def scrap(url):
    print(colored("[COMMAND]","blue"),"The 'scrap' command was requested for the url:",url)
    source = urllib.request.urlopen(url)
    soup = BeautifulSoup(source, 'html.parser')
    first_paragraph = soup.p.getText()
    await bot.say("```"+first_paragraph+"```")

# running the bot
try:
    # if user inputs a valid token, the bot will start
    bot_token = input("For the bot to run, please insert a valid token: ")
    # starts the bot
    bot.run(bot_token)
    #checks for valid token
except discord.errors.LoginFailure:
    print(colored("[ERROR]","red"),"Please enter a valid token!")
    time.sleep(1)
    sys.exit()
