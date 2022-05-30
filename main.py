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
import numpy as np

intents = discord.Intents.default()
intents.members = True
load_dotenv()
bot = commands.Bot(command_prefix='+', intents=intents)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_member_remove(member):
    guild = member.guild
    await member.send('Sorry to see you leave so soon :(')


@bot.event
async def on_member_join(member):
    guild = member.guild
    ##channel = discord.utils.get(member.guild.channels)
    ##await channel.send(f'Everyone, welcome {member.name} to the server! :confetti:')
    embed = discord.Embed(title='Welcome!', description=f'Welcome to the {guild.name} server! :partying_face:', color=discord.Color.blue())
    await member.send(embed=embed)




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
        await ctx.send("The main weather is: " + response["weather"][0]["main"] + '\n' +
                       "Description: " + response["weather"][0]["description"] + '\n' +
                       "The current temperature is " + str(response["main"]["temp"]) + '\n' +
                       "Feels like " + str(response["main"]["feels_like"]) + "\u00b0F")

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
        if anime_name == '86':
            response = jikan.anime(41457)
            title = response['title'] + " / " + str(response['title_english']) + " (" + response['status'] + ')'
            embed = discord.Embed(title=title, url=response['url'], description=response['synopsis'], color=discord.Color.blue())
            embed.set_thumbnail(url=response['image_url'])
            embed.add_field(name='Episodes: ', value=str(response['episodes']), inline=True)
            embed.add_field(name='Score: ', value=str(response['score']) + "/10 :star:", inline=True)
            embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
            await ctx.send(embed=embed)
        elif isinstance(int(anime_name), int) == True:
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
        try:
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
        except:
            n=0
            suggested = []
            for i in response['results']:
                suggested.append((response['results'][n]['title']))
                n += 1

            embedSuggest = discord.Embed(title="Did you mean: ", description=listToString(suggested), color=discord.Color.blue())
            await ctx.send(embed=embedSuggest)
@bot.command()
async def manga(ctx, *manga):
    manga_name = ''.join(manga)
    print(manga_name)
    # title, title_english, status, image_url, chapters, volumes, score, synopsis,url,
    try:
        if manga_name == '86':
            response = jikan.manga(112236)
            title = response['title'] + " / " + str(response['title_english']) + " (" + response['status'] + ')'
            embed = discord.Embed(title=title, url=response['url'], description=response['synopsis'], color=discord.Color.blue())
            embed.set_thumbnail(url=response['image_url'])
            embed.add_field(name='Volumes: ', value=str(response['volumes']), inline=True)
            embed.add_field(name='Chapters: ', value=str(response['chapters']), inline = True)
            embed.add_field(name='Score: ', value=str(response['score']) + "/10 :star:", inline=True)
            embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
            await ctx.send(embed=embed)
        elif isinstance(int(manga_name), int) == True:
            response = jikan.anime(manga_name)
            print(response)
            title = response['title'] + " / " + str(response['title_english']) + " (" + response['status'] + ')'
            embed = discord.Embed(title=title, url=response['url'], description=response['synopsis'], color=discord.Color.blue())
            embed.set_thumbnail(url=response['image_url'])
            embed.add_field(name='Volumes: ', value=str(response['volumes']), inline=True)
            embed.add_field(name='Chapters: ', value=str(response['chapters']), inline = True)
            embed.add_field(name='Score: ', value=str(response['score']) + "/10 :star:", inline=True)
            embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
            await ctx.send(embed=embed)
    except:
        manga_name = ''.join(manga)
        manga_name = manga_name.lower()
        response = jikan.search('manga', manga_name)
        print(response)
        x = 0
        try:
            while response['results'][x]['title'].replace(" ", '').lower() != manga_name:
                print(response['results'][x]['title'])
                x += 1
            print(response['results'][x]['title'])
            manga_name = response['results'][x]['mal_id']
            response = jikan.manga(manga_name)
            print(response)
            title = response['title'] + " / " + str(response['title_english']) + " (" + response['status'] + ')'
            embed = discord.Embed(title=title, url=response['url'], description=response['synopsis'],
                              color=discord.Color.blue())
            embed.set_thumbnail(url=response['image_url'])
            embed.add_field(name='Volumes: ', value=str(response['volumes']), inline=True)
            embed.add_field(name='Chapters: ', value=str(response['chapters']), inline = True)
            embed.add_field(name='Score: ', value=str(response['score']) + "/10 :star:", inline=True)
            embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
            await ctx.send(embed=embed)
        except:
            n=0
            suggested = []
            for i in response['results']:
                suggested.append((response['results'][n]['title']))
                n += 1

            embedSuggest = discord.Embed(title="Did you mean: ", description=listToString(suggested), color=discord.Color.blue())
            await ctx.send(embed=embedSuggest)
@bot.command()
async def pfp(ctx, member: discord.Member = None):
    if member == None:
        user = ctx.message.author
        pfp = user.avatar_url
        await ctx.send(pfp)
    else:
        pfp = member.avatar_url
        await ctx.send(pfp)

def listToString(s):
    str1 = " \n"
    return str1.join(s)


bot.run(os.getenv('TOKEN'))
