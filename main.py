import time
import datetime
import discord
from discord.utils import get
from discord.ext import commands
import os
from dotenv import load_dotenv
import requests
import random
from jikanpy import Jikan


intents = discord.Intents.default()
intents.members = True
load_dotenv()
bot = commands.Bot(command_prefix='+', intents=intents)


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

@bot.command()
async def magicball(ctx, *question):
    question_full = ' '.join(question)
    responses = ['It is certain.' ,
                 'It is decidedly so.' ,
                 'Without a doubt.' ,
                 'Yes definitely.' ,
                 'You may rely on it.' ,
                 'As I see it, yes.' ,
                 'Most likely.' ,
                 'Outlook good.' ,
                 'Yes.' ,
                 'Signs point to yes.' ,
                 'Reply hazy, try again.' ,
                 'Ask again later.' ,
                 'Better not tell you now.' ,
                 'Cannot predict now.' ,
                 'Concentrate and ask again.' ,
                 "Don't count on it." ,
                 'My reply is no.' ,
                 'My sources say no.' ,
                 'Outlook not so good.']
    response = random.choice(responses)
    embed=discord.Embed(title="The Magic Being, BotBot, has spoken!")
    embed.add_field(name='Question: ', value=f'{question_full}', inline=True)
    embed.add_field(name='Answer: ', value=f'{response}', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def flip(ctx):
    answers = ['heads', 'tails']
    num = random.randint(0, 1)
    if(num == 0):
        await ctx.send(answers[0])
    else:
        await ctx.send(answers[1])

@bot.command()
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send('Bot joined')
    else:
        await ctx.send("You must be in a voice channel first so I can join it.")

@bot.command()
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send('Bot left')
    else:
        await ctx.send("I'm not in a voice channel, use the join command to make me join")


jikan = Jikan()
@bot.command()
async def anime(ctx,*anime):
    anime_name = ''.join(anime)
    print(anime_name)
    try:
        if isinstance(int(anime_name), int) == True:
            response = jikan.anime(anime_name)
            print(response)
            title = response['title'] + " / " + str(response['title_english']) + " (" + response['status'] + ')'
            embed = discord.Embed(title=title, url=response['url'], description=response['synopsis'], color=discord.Color.blue())
            embed.set_thumbnail(url=response['image_url'])
            embed.add_field(name='Episodes: ', value=str(response['episodes']), inline=True)
            embed.add_field(name='Score: ', value=str(response['score']) + "/10 :star:", inline=True)
            embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
            await ctx.send(embed=embed)
    except:
        anime_name = ''.join(anime)
        anime_name = anime_name.lower()
        print(anime_name)
        response = jikan.search('anime', anime_name)
        print(response)
        x = 0
        while response['results'][x]['title'].replace(" ", '').lower() != anime_name:
            print(response['results'][x]['title'])
            x += 1
        print(response['results'][x]['title'])
        anime_name = response['results'][x]['mal_id']
        response = jikan.anime(anime_name)
        print(response)
        title = response['title'] + " / " + str(response['title_english']) + " (" + response['status'] + ')'
        embed = discord.Embed(title=title, url=response['url'], description=response['synopsis'],
                              color=discord.Color.blue())
        embed.set_thumbnail(url=response['image_url'])
        embed.add_field(name='Episodes: ', value=str(response['episodes']), inline=True)
        embed.add_field(name='Score: ', value=str(response['score']) + "/10 :star:", inline=True)
        embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
        await ctx.send(embed=embed)




bot.run(os.getenv('TOKEN'))