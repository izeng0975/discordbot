import time
import datetime
import discord
from discord.utils import get
intents = discord.Intents.default()
intents.members = True
from discord.ext import commands
import os

from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix='.', intents = intents)
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

#@bot.event
#async def on_message(message):
 #   if message.author == bot.user:
 #       return
#
  #  if message.content == 'hello':
  #      await message.channel.send('HELLO!')

#@bot.event
#async def on_member_join(member):
    #mbed = discord.Embed(
        #colour = (discord.Colour.magenta()),
        #title = 'Welcome Message',
        #description = f'Welcome {member.mention}, enjoy your stay !'
    #)
    #print("Recognised that a member called " + member.name + " joined")

@bot.event
async def on_member_join(member):
    ##embed = discord.Embed(colour = 0x95efcc, description = f'Welcome to {guild.name}! You are the {len(list(member.guild.members))} member!')
    ##embed.set_thumbnail(url = f'{member.avatar_url}')
    ##embed.set_author(name = f'{member.name}', icon_url=f'{member.avatar_url}')
    ##embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
    guild = member.guild
    ##guild = bot.get_guild(976646664360198144)
    ##channel = discord.utils.get(member.guild.channels)
    channel = guild.get_channel(976646664976752672)
    await channel.send(f'Everyone, welcome {member.name} to the server! :confetti:')
    await member.send(f'Welcome to the {guild.name} server, {member.name}! :sunglasses: ')
    ##await channel.send(f'Everyone, welcome {member.name} to the server! :confetti:')
    ##await channel.send(embed = embed)
#@bot.event
#async def on_message(message):
 #   messageCont = message.content.lower()
#    if message.author == bot.user:
 #       return
 #   if messageCont == 'lol':
 #       print(message.author.id)
 #       await message.channel.send(message.author.mention)

@bot.command()
async def spam(ctx, content, num: int):
    for i in range(num):
        await ctx.send(content)
        time.sleep(0.5)


bot.run(os.getenv('TOKEN'))
