import time
import datetime
import discord
from discord.utils import get
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests

intents = discord.Intents.default()
intents.members = True
load_dotenv()
bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_member_leave(member):
    guild = member.guild
    channel = guild.get_channel(member.guild.channels)
    await channel.send(f'Everyone, {member.name} has left the server. :sad:')
    await member.send('Sorry to see you leave so soon :(')


@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(member.guild.channels)
    await channel.send(f'Everyone, welcome {member.name} to the server! :confetti:')
    await member.send(f'Welcome to the {guild.name} server, {member.name}! :sunglasses: ')


'''@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        embed = discord.Embed(title=f'Please repeatedly mention <@294545296921460737>', color=discord.Color.green())
        await message.channel.send(embed=embed)
        await message.channel.send('<@294545296921460737>')'''



@bot.command()
async def spam(ctx, num: int, *message):
    for i in range(num):
        await ctx.send(' '.join(message))
        time.sleep(0.5)


@bot.command()
async def weather(ctx, *city):
    city_full = ' '.join(city)
    global response
    url = os.getenv('weather_url')
    api_key = os.getenv('weather_api_key')
    querystring = {"q": city_full, "appid": api_key, "units": "imperial"}
    response = requests.request("GET", url, params=querystring)
    response = response.json()
    print(response)
    if 'message' in response:
        if response['message'] == 'city not found':
            await ctx.send("That's not a real place!")
    else:
        await ctx.send("The main weather is: " + response["weather"][0]["main"])
        await ctx.send("Description: " + response["weather"][0]["description"])
        await ctx.send("The current temperature is " + str(response["main"]["temp"]) +"\u00b0F")
        await ctx.send("Feels like " + str(response["main"]["feels_like"]) +"\u00b0F" )




bot.run(os.getenv('TOKEN'))