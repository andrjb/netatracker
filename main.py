# author:       andrjb
# date:         2022-02-10
# description:  A simple Discord bot that pulls the current NETA/ERG price from the                     ergoDEX API. Can be used as sidebar bot and can send current price in a                 message on command.
#---------------------------------------------------------------------------------
import discord
import asyncio
import os
from discord.ext import tasks
from keepalive import keepalive
from api_functions import get_price, erg_price, ada_price, buildtable
from blockfrost import pool, cneta
client = discord.Client()
#---------------------------------------------------------------------------------
try: 
  #Initial things once the bot starts up
  @client.event
  async def on_ready():
      print('Logged in as {0.user}'.format(client))
      update_activity.start()
      stickynote.start()
#---------------------------------------------------------------------------------

#Checks if someone sends a "$" if that's the case, it sense price information as message
  @client.event
  async def on_message(message):
      if message.author == client.user:
          return

      if message.content.startswith('!usd'):
          netergprice, ergnetprice, pricestat = get_price()
          cnetaprice, cnetatstat = cneta()
          erg, ergstat = erg_price()
          ada, adastat = ada_price()
          if ergstat + pricestat + adastat + cnetatstat == 800:
            s = "\nERG: "+str(erg)+" $" +"\nNETA/USD: "+str(round(ergnetprice*erg,5))+" $" "\nADA price: "+str(ada)+" $"+"\ncNETA/USD: " +str(round(cnetaprice*ada,5))+"$"
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
          await message.channel.send(s)
        else:
          await message.channel.send("Couldn't retrieve price from api. Try again later")

      if message.content.startswith('!cneta'):
        cnetaprice, cnetatstat = cneta()
        if cnetatstat == 200:
          s = "cNETA/ADA: " + str(cnetaprice) + " ADA"
          await message.channel.send(s)
        else:
          await message.channel.send("Couldn't retrieve price from api. Try again later")
            
      if message.content.startswith('$'):
        await message.channel.send(":robot: New features introduced :robot:. beepboop\nThis command is outdated. Please use the following commands:\n!neta -> returns neta price\n!cneta -> returns cneta price\n!usd -> returns erg and neta price in dollars\n!stake -> returns total stake in LISO pools")
#---------------------------------------------------------------------------------

#"stickynote" a table with all prices will be posted every 30s as most recent post
  @tasks.loop(seconds=30)
  async def stickynote():
      channel = client.get_channel(920108802534178876)
      netergprice, ergnetprice, s1 = get_price()
      cnetaprice, s2 = cneta()
      erg, s3 = erg_price()
      ada, s4 = ada_price()
      if s1 + s2 + s3 + s4 == 800:
        s = buildtable(netergprice, ergnetprice, cnetaprice, erg, ada)
        await(await channel.send(s)).delete(delay=29)
        print("updated list")
      else:
        print("Couldn't retrieve price from api. Try again later")
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

  keepalive()
  client.run(os.getenv('TOKEN'))
except:
  pass
