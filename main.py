# author:       andrjb
# date:         2022-02-08
# description:  A simple Discord bot that pulls the current NETA/ERG price from the                     ergoDEX API. Can be used as sidebar bot and can send current price in a                 message on command.
#---------------------------------------------------------------------------------
import discord
import os
import requests
import json
from discord.ext import tasks
from keepalive import keepalive
client = discord.Client()
#---------------------------------------------------------------------------------

#Detects and cuts out the amount of tokens in liquidity pool (from API call)
def cut_amount(string):
  index = string.find("amount")
  val = ""
  for i in range(index + 9, len(string)):
    val += string[i]
    if string[i+1] == ',': 
      break 
  string = int(val) 
  return(string)
#---------------------------------------------------------------------------------

#Makes API call and calculates price with amount of tokens in LP
def get_price():
    response = requests.get(
        "https://api.ergodex.io/v1/amm/pool/7d2e28431063cbb1e9e14468facc47b984d962532c19b0b14f74d0ce9ed459be/stats?from"
    )
    if int(response.status_code) == 200:
      json_data = json.loads(response.text)
      result = json.dumps(json_data)
      ERGamount = str(result[150:200])     #170:185 contains amount (unstable)
      ERGamount = cut_amount(ERGamount)
      NETAamount = str(result[295:345])     #170:185 contains amount (unstable)
      NETAamount = cut_amount(NETAamount)
      netergprice = round(((NETAamount / ERGamount) * 1000), 8)
      ergnetprice = round(((ERGamount / NETAamount) / 1000), 8)
      return (netergprice, ergnetprice, int(response.status_code))
    else: 
      print("Error occured: " + str(response.status_code))
      return(0, 0, int(response.status_code))
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

    if message.content.startswith('$'):
        netergprice, ergnetprice, stat = get_price()
        if stat == 200:
          s = 'NETA per ERG: ' + str(
              netergprice) + "\n" + 'ERG per NETA: ' + str(ergnetprice)
          await message.channel.send(s)
        else:
          await message.channel.send("Couldn't retrieve price from api. Try again later")
#---------------------------------------------------------------------------------

#updates the current NETA/ERG valuation as "playing" activity of the bot (every minute)
@tasks.loop(seconds=30.0)
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
