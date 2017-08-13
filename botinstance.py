#-*- coding : utf-9 -*-
"""
Author: Sturza Mihai
GitHub: https://github.com/MArtzDEV
"""

import discord, urllib.request,asyncio, sys, time
from discord.ext import commands
from bs4 import BeautifulSoup
from termcolor import colored
from google import search

# creates the bot instance
    # adds the prefix
prefix = "<>"
bot = commands.Bot(prefix)

# ignore this
music_player = None
voice_connect = None

# prints some info about the bot after loggin in on the discord servers
@bot.event
@asyncio.coroutine
def on_ready():
    print("Commands will be displayed with",colored('blue','blue'),"errors with",colored('red','red'),"and bot the bot status with",colored('green','green'))
    print(colored("[LOGIN]","green"),"Logged in as {}".format(bot.user.name))

"""
########
COMMANDS
########
"""
@bot.event
@asyncio.coroutine
async def on_message(message):
    """
    ###########
    MUSIC PLAYER
    ###########
    """
    if message.content.split()[0] == prefix + "music":
        if message.content.split()[1] == "play":
            print(colored("[COMMAND]",'blue'),"The 'music play' command was requested for the url:",message.content.split()[2])
            await bot.send_message(message.channel,"Playing the requested song.")
            try:
                global voice_connect
                voice_connect = await bot.join_voice_channel(message.author.voice.voice_channel)
                global music_player
                music_player = await voice_connect.create_ytdl_player(message.content.split()[2])
                music_player.start()
                # sometimes it CAN happen
            except discord.ClientException:
                music_player = await voice_connect.create_ytdl_player(message.content.split()[2])
                music_player.start()
        # stopping the player
        elif message.content.split()[1] == "stop":
            print(colored("[COMMAND]",'blue'),"The 'music stop' command was requested")
            await bot.send_message(message.channel,"Stopping the requested song.")
            music_player.stop()
        # raising or lowering the volume
        elif message.content.split()[1] == "volume":
            print(colored("[COMMAND]",'blue'),"The 'music volume' command was requested")
            await bot.send_message(message.channel,"Adjusting the volume of the song.")
            music_player.volume = float(message.content.split()[2])/100;
    """
    ############
    WEB COMMANDS
    ############
    """
    if message.content.split()[0] == prefix + "web":
        # web scrapping command
        if message.content.split()[1] == "scrap":
            print(colored("[COMMAND]","blue"),"The 'scrap' command was requested for the url:",message.content.split()[2])
            source = urllib.request.urlopen(message.content.split()[2])
            soup = BeautifulSoup(source, 'html.parser')
            first_paragraph = soup.find('p').getText()
            await bot.send_message(message.channel,"```"+first_paragraph+"```")
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
