import discord
import os
import requests
import json
from discord.ext import tasks
from keepalive import keepalive
client = discord.Client()

def get_price():
    response = requests.get(
        "https://api.ergodex.io/v1/amm/pool/7d2e28431063cbb1e9e14468facc47b984d962532c19b0b14f74d0ce9ed459be/stats?from"
    )
    json_data = json.loads(response.text)
    result = json.dumps(json_data)
    ERGamount = int(result[170:185])     #170:185 contains amount
    NETAamount = int(result[315:329])    #315:329 contains amount
    # make this more stable ^
    netergprice = round(((NETAamount / ERGamount) * 1000), 6)
    ergnetprice = round(((ERGamount / NETAamount) / 1000), 6)
    return (netergprice, ergnetprice)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    update_activity.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$'):
        netergprice, ergnetprice = get_price()
        s = 'Neta per ERG: ' + str(
            netergprice) + "\n" + 'ERG per NETA: ' + str(ergnetprice)
        await message.channel.send(s)

@tasks.loop(minutes=1)
async def update_activity():
  netergprice, ergnetprice = get_price()
  activity = str(round(netergprice, 3)) + ' NETA/ERG'
  await client.change_presence(activity=discord.Game(activity))

keepalive()
client.run(os.getenv('TOKEN'))
