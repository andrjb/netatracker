# author:       andrjb
# date:         2022-02-10
# description:  A simple Discord bot that pulls the current NETA/ERG price from the                     ergoDEX API. Can be used as sidebar bot and can send current price in a                 message on command.
#---------------------------------------------------------------------------------
import discord
import os
from discord.ext import tasks
from keepalive import keepalive
from api_functions import get_price, erg_price
from blockfrost import pool, cneta
client = discord.Client()
#---------------------------------------------------------------------------------

#Initial things once the bot starts up
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    update_activity.start()
#---------------------------------------------------------------------------------

#Checks if someone sends a "$" if that's the case, it sense price information as message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!usd'):
        netergprice, ergnetprice, pricestat = get_price()
        erg, ergstat = erg_price()
        if ergstat + pricestat == 400:
          s = "\nERG: "+str(erg)+" $, " +"NETA: "+str(round(ergnetprice*erg,5))+" $"
          await message.channel.send(s)
        else:
          await message.channel.send("Couldn't retrieve price from api. Try again later")

    if message.content.startswith('!neta'):
        netergprice, ergnetprice, netastat = get_price()
        if netastat == 200:
          s = 'NETA/ERG: ' + str(
              netergprice) + "\n" + 'ERG/NETA: ' + str(ergnetprice)
          await message.channel.send(s)
        else:
          await message.channel.send("Couldn't retrieve price from api. Try again later")

    if message.content.startswith('!stake'):
      s, stakestat = pool()
      if stakestat == 400:
        s = "LISO total stake: " + str(s) + " ADA"
        print(s)
        await message.channel.send(s)
      else:
        await message.channel.send("Couldn't retrieve price from api. Try again later")

    if message.content.startswith('!cneta'):
      s, cnetatstat = cneta()
      if cnetatstat == 200:
        s = "cNETA/ADA: " + str(s) + " ADA"
        print(s)
        await message.channel.send(s)
      else:
        await message.channel.send("Couldn't retrieve price from api. Try again later")
          
    if message.content.startswith('$'):
      await message.channel.send(":robot: New features introduced :robot:. beepboop\nThis command is outdated. Please use the following commands:\n!neta -> returns neta price\n!cneta -> returns cneta price\n!usd -> returns erg and neta price in dollars\n!stake -> returns total stake in LISO pools")
    
#---------------------------------------------------------------------------------

#updates the current NETA/ERG valuation as "playing" activity of the bot (every minute)
@tasks.loop(seconds=60)
async def update_activity():
  netergprice, ergnetprice, stat = get_price()
  if stat == 200:
    activity = str(round(netergprice, 3)) + ' NETA/ERG'
    await client.change_presence(activity=discord.Game(activity))
    print(activity)
  else:
    print("Error couldn't retrieve data from api, keep last data")
#---------------------------------------------------------------------------------

update_activity.start()
keepalive()
client.run(os.getenv('TOKEN'))
