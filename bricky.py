# bot.py
import os
import json
import requests

import subprocess
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
APIKEY = os.getenv('apiKey')
USERNAME = os.getenv('username')
PASSWORD = os.getenv('password')


#print('TOKEN = ',TOKEN)
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    args = message.content.split()

    if message.author == client.user:
        return


    if message.content == '!test':
        response = 'dit werkt!'
        await message.channel.send(response)

    if message.content.startswith('!set'):
        returnstring, smallimage = get_set(args[1])
        embed = discord.Embed(title=args[1], color=0x309bf3)
        embed.set_image(url=smallimage)
        embed.set_footer(text=returnstring)
        await message.channel.send(embed=embed)

    if message.content.startswith('!bw'):
        print("got !bw")
        filename="Brickwatch"+args[1]
        output = get_brickwatchimage(args[1])
        print(output)
        await message.channel.send(file=discord.File('~/bot/bw.png'))

def get_set(setnumber):
    url = 'https://brickset.com/api/v3.asmx/login'
    params = {'apiKey': APIKEY,'username':USERNAME,'password':PASSWORD}
    x = requests.post(url, data = params)

    json_data = json.loads(x.text)
    hash = json_data["hash"]

    url = 'https://brickset.com/api/v3.asmx/getSets'
    params = {'apiKey': APIKEY,'userHash':hash,'params':"{'setNumber':'"+setnumber+"-1'}"}
    x = requests.post(url, data = params)

    json_data = json.loads(x.text)

    #get the sets part
    set = json_data["sets"]
    #get the first match
    subset= set[0]
    #getthedata
    name =subset["name"]
    year = str(subset["year"])
    setnumber = subset["number"]
    pieces = str(subset["pieces"])
    images = subset["image"]
    smallimage=images["imageURL"]


    returnstring=setnumber+" - "+name+" ("+year+") - "+pieces+"pcs "

    return returnstring, smallimage


def get_brickwatchimage(setnumber):
    bashCommand = '/usr/bin/google-chrome --headless --disable-gpu --screenshot="~/bot/bw.png" --hide-scrollbars --user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36" --window-size=600,800 https://www.brickwatch.net/nl-BE/set/'+setnumber+'?order=p'
    print(bashCommand)
    output = os.system(bashCommand)
#    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
#    output, error = process.communicate()
    return output

client.run(TOKEN)
