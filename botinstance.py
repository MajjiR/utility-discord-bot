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
from datetime import datetime

"""
!!! IMPORTANT !!!
    -Before using any command, please add the right permissons for the bot !
"""
# creates the bot instance
    # adds the prefix
prefix = "<>"
bot = commands.Bot(prefix)

# ignore this
music_player = None
voice_connect = None
start_time = None

# prints some info about the bot after loggin in on the discord servers
@bot.event
@asyncio.coroutine
def on_ready():
    #checks the start time
    global start_time
    start_time = datetime.now()
    print("Commands will be displayed with",colored('blue','blue'),"events with",colored('yellow','yellow'),"errors with",colored('red','red'),"and bot the bot status with",colored('green','green'))
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

    """
    ############
    BOT COMMANDS
    ############
    """
    if message.content.split()[0] == prefix + "bot":
        # shows the creator of the bot - Sturza Mihai
        if message.content.split()[1] == "author":
            await bot.send_message(message.channel,"The creator of this bot is Sturza Mihai\n- https://martzdev.github.io/martz-portfolio/\n- https://github.com/MArtzDEV")
        # calculates the bot's uptime
        if message.content.split()[1] == "uptime":
            print(colored("[COMMAND]","blue"),"The 'uptime' command was used.")
            check_time = datetime.now()
            uptime_h = check_time.hour - start_time.hour
            uptime_m = check_time.minute - start_time.minute
            uptime_s = check_time.second - start_time.second
            await bot.send_message(message.channel,"{0} has been up for {1} : {2} : {3}.".format(bot.user.name,uptime_h,uptime_m,uptime_s))
            print(colored("[UPTIME]","green"),"{0} has been up for {1} : {2} : {3}.".format(bot.user.name,uptime_h,uptime_m,uptime_s))

"""
######
EVENTS
######
"""
@bot.event
@asyncio.coroutine
async def on_member_join(member):
    # prints a message when a user joins
    print(colored("[MEMBER]","yellow"),"{0} has joined {1}".format(member.user.name,member.server))
    welcome_message = "Welcome {0} to {1}! I hope you'll have fun here!".format(member.user.name,member.server)
    channel = bot.get_channel("312091724681969676") # INPUT HERE YOUR WELCOME CHANNEL
    await bot.send_message(channel,welcome_message)
@bot.event
@asyncio.coroutine
async def on_member_remove(member):
    # prints a message when a user leaves
    print(colored("[MEMBER]","yellow"),"{0} has left {1}".format(member.user.name,member.server))
    goodbye_message = "Goodbye {0}.I hope you'll rejoin {1} soon!".format(member.user.name,member.server)
    channel = bot.get_channel("312091724681969676") # INPUT HERE YOUR WELCOME CHANNEL
    await bot.send_message(channel,goodbye_message)


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
