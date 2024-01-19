import json
import requests
import discord
from discord.ext import commands
from datetime import datetime
import schedule
import asyncio

#Your discord bot token
TOKEN_BOT = "your_token"

#lang = "fr" or "en" or others
lang = "set_me"

#Discord channel in which the message will be send
channel_name = "set_me"

#Basic intents for discord bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready !")

    #"""
    #Message schedule everydady at X o'clock 
    schedule.every().day.at("00:01").do(send_daily_message)

    #We use asyncio over time.sleep for cpu uses reasons
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)
    #"""

    #If you want to make a test of your message, uncomment lines 27, 35 and 38
    #send_daily_message()

#Function to keep information about daily almanax and send them in a discord channel
def send_daily_message():

    date_en = datetime.now().strftime("%Y-%m-%d") #Needed for the request
    date_fr = datetime.now().strftime("%d/%m/%Y") #Don't required, in this case use for the message

    #Request to get daily almanax information
    url = f"https://alm.dofusdu.de/dofus/{lang}/{date_en}"
    response = requests.get(url)
    response_data = response.json()

    #Set important information into variable, if you want more information check this : https://alm.dofusdu.de/swagger/
    daily_bonus = response_data["data"]["bonus"]["bonus"]
    daily_bonus_description = response_data["data"]["bonus"]["description"]
    item_name = response_data["data"]["item_name"]
    item_quantity = response_data["data"]["item_quantity"]

    #Message_exemple = f"\n---------------------------------------------------------------------------------- 🥚 {date_fr} 🥚 ---------------------------------------------------------------------------------- \n\n🌍 Le bonus du jour est '{daily_bonus}' : {daily_bonus_description} \n✅ Il faut ramener {item_quantity} {item_name}. \n\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
    message = "set_me"

    #Message will be send in the discord channel set up before
    channel = discord.utils.get(bot.get_all_channels(), name=channel_name)
    if channel:
        bot.loop.create_task(channel.send(message))
        print ("Message send in discord channel.") #Validation in the terminal when the message is send

bot.run(TOKEN_BOT)