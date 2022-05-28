import time
import random
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


@bot.command()
async def magicball(ctx, *question):
    question_full = ' '.join(question)
    responses = ['As I see it, yes.',
             'Yes.',
             'Positive',
             'From my point of view, yes',
             'Convinced.',
             'Most Likley.',
             'Chances High',
             'No.',
             'Negative.',
             'Not Convinced.',
             'Perhaps.',
             'Not Sure',
             'Mayby',
             'I cannot predict now.',
             'Im to lazy to predict.',
             'I am tired. *proceeds with sleeping*']
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
    else: #But is (s)he isn't in a voice channel
        await ctx.send("You must be in a voice channel first so I can join it.")

@bot.command()
async def leave(ctx): 
    if (ctx.voice_client): 
        await ctx.guild.voice_client.disconnect() 
        await ctx.send('Bot left')
    else: # But if it isn't
        await ctx.send("I'm not in a voice channel, use the join command to make me join")


bot.run(os.getenv('TOKEN'))
