import datetime
from datetime import datetime, timedelta
import string
import uuid
import time
from datetime import date
import discord
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ext.commands import BadArgument
from discord.ext.commands import CommandInvokeError
from discord.ext.commands import MissingRequiredArgument
from dotenv import load_dotenv
import requests
import random
from jikanpy import Jikan
import numpy as np
import os
import openai
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import youtube_dl
import asyncio
import deeppyer
from io import BytesIO, StringIO





intents = discord.Intents.all()
intents.members = True
load_dotenv()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='+', intents=intents, activity=discord.Activity(type=discord.ActivityType.listening, name="+help"))
bot.remove_command('help')

numbers="1️⃣", "2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.group(invoke_without_command=True)
async def help(ctx):
    embed= discord.Embed(title='Help', description='Use +help <command> for extended information on a command', color=ctx.author.color)
    embed.add_field(name='Moderation', value='kick, ban, clear', inline=True)
    embed.add_field(name='Fun', value='magicball, chat, notes, spam, flip, pfp, poll, deepfry, rps, password_gen', inline=False)
    embed.add_field(name='Useful info', value='userinfo, serverinfo, weather, anime, manga', inline=False)
    embed.add_field(name='Music', value='join, leave, play, stop, resume, pause', inline=False)
    await ctx.send(embed=embed)

@help.command()
async def kick(ctx):
    embed=discord.Embed(title='Kick', description='Kicks a member from the server', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+kick <member> [reason(optional)]')
    await ctx.send(embed=embed)

@help.command()
async def ban(ctx):
    embed=discord.Embed(title='Ban', description='Bans a member from the server', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+ban <member> [reason(optional)]')
    await ctx.send(embed=embed)

@help.command()
async def clear(ctx):
    embed=discord.Embed(title='Clear', description='Deletes specified number of messages', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+clear <number>')
    await ctx.send(embed=embed)

@help.command()
async def magicball(ctx):
    embed=discord.Embed(title='Magic 8 Ball', description='The spooky, magical, magic 8 ball will answer any question', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+magicball <question>')
    await ctx.send(embed=embed)

@help.command()
async def chat(ctx):
    embed=discord.Embed(title='Chat', description='Can interact with the bot by asking it questions', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+chat <question>')
    await ctx.send(embed=embed)

@help.command()
async def notes(ctx):
    embed=discord.Embed(title='Notes', description='Ask the bot for up to 5 notes on a certain topic', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+notes What are <up to 5> notes on <topic>?')
    await ctx.send(embed=embed)

@help.command()
async def spam(ctx):
    embed=discord.Embed(title='Spam', description='Tell the bot to spam a certain message a given amount of times', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+spam <num> <message>')
    await ctx.send(embed=embed)

@help.command()
async def flip(ctx):
    embed=discord.Embed(title='Flip', description='Tell the bot to flip a coin', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+flip')
    await ctx.send(embed=embed)

@help.command()
async def pfp(ctx):
    embed=discord.Embed(title='Profile Picture', description='Tell the bot to send back the profile picture of you or requested member', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+pfp <member> [+pfp will return your own]')
    await ctx.send(embed=embed)

@help.command()
async def poll(ctx):
    embed=discord.Embed(title='Poll', description='Tell the bot to create a poll. Up to 9 choices are allowed.', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+poll "<Question>" choices', inline=True)
    embed.add_field(name='Example', value='+poll "Fortnite or PUBG?" fortnite pubg none')
    await ctx.send(embed=embed)

@help.command()
async def deepfry(ctx):
    embed=discord.Embed(title='Deepfry', description='Bot will return a deepfried image of attachment sent. Must be an image, not URLs', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+deepfry [attach image while sending]')
    await ctx.send(embed=embed)

@help.command()
async def rps(ctx):
    embed=discord.Embed(title='Rock Paper Scissor', description='Play rock, paper, scissors with the bot', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+rps <rock, paper, scissors>')
    await ctx.send(embed=embed)

@help.command()
async def password_gen(ctx):
    embed=discord.Embed(title='Password Generator', description='Bot will create a secure password and DM you it', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+password_gen')
    await ctx.send(embed=embed)

@help.command()
async def userinfo(ctx):
    embed=discord.Embed(title='User Information', description='Information about a specified user will be sent', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+userinfo <member> [+userinfo will send userinfo about caller]')
    await ctx.send(embed=embed)

@help.command()
async def serverinfo(ctx):
    embed=discord.Embed(title='Server Information', description='Information about server will be sent', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+serverinfo')
    await ctx.send(embed=embed)

@help.command()
async def weather(ctx):
    embed=discord.Embed(title='Weather Information', description='Information about specified place will be sent as image', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+weather <place>')
    await ctx.send(embed=embed)

@help.command()
async def anime(ctx):
    embed=discord.Embed(title='Anime Information', description='Information about specified anime will be sent', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+anime <anime name>')
    await ctx.send(embed=embed)

@help.command()
async def manga(ctx):
    embed=discord.Embed(title='Manga Information', description='Information about specified manga will be sent', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+anime <manga name>')
    await ctx.send(embed=embed)

@help.command()
async def play(ctx):
    embed=discord.Embed(title='Play Music', description='Will play song from given URL', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+play <URL> [Must do +join first!]')
    await ctx.send(embed=embed)

@help.command()
async def join(ctx):
    embed=discord.Embed(title='Join Voice Channel', description='Will join voice channel caller is in', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+join [this must be used before doing +play]')
    await ctx.send(embed=embed)

@help.command()
async def leave(ctx):
    embed=discord.Embed(title='Leave Voice Channel', description='Will leave bot is in', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+leave')
    await ctx.send(embed=embed)

@help.command()
async def stop(ctx):
    embed=discord.Embed(title='Stop Music', description='Will stop the music that is currently playing', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+stop')
    await ctx.send(embed=embed)

@help.command()
async def pause(ctx):
    embed=discord.Embed(title='Pause Music', description='Will pause the music that is currently playing', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+pause')
    await ctx.send(embed=embed)

@help.command()
async def resume(ctx):
    embed=discord.Embed(title='Resume Music', description='Will resume the music that is currently paused', color=ctx.author.color)
    embed.add_field(name='**Syntax**', value='+resume')
    await ctx.send(embed=embed)




@bot.command(name='spam', help='Spam any given string message - - - Format:+spam 5 hello i am cool')
async def spam(ctx, num: int, *message):
    for i in range(num):
        await ctx.send(' '.join(message))
        time.sleep(0.5)

@spam.error
async def spam_error(ctx, error):
    if isinstance(error, BadArgument):
        await ctx.send('Please input a number!')

@bot.command()
async def weather(ctx, *city):
    city_full = ' '.join(city)
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
        image = Image.open("post.png")
        draw = ImageDraw.Draw(image)
        #title and subheading
        font = ImageFont.truetype("Inter.ttf", size=40)
        content = "Latest Weather Forecast for " + response['name']
        color = "rgb(255, 255, 255)"
        (x, y) = (46, 74)
        draw.text((x, y), content, color, font=font)

        font = ImageFont.truetype("Inter.ttf", size=35)
        today = date.today()
        content = today.strftime("%A - %B %d, %Y")
        color = "rgb(255, 255, 255)"
        (x, y) = (46, 145)
        draw.text((x, y), content, color, font=font)

        #temperature
        font = ImageFont.truetype("Inter.ttf", size=40)
        color = "rgb(0, 0, 0)"
        (x, y) = (135, 300)
        draw.text((x, y), "The main weather is:", color, font=font)

        font = ImageFont.truetype("Inter.ttf", size=40)
        content = str(response["weather"][0]["main"])
        color = "rgb(255, 255, 255)"
        (x, y) = (650, 300)
        draw.text((x, y), content, color, font=font)

        #weather description
        font = ImageFont.truetype("Inter.ttf", size=40)
        color = "rgb(0, 0, 0)"
        (x, y) = (135, 430)
        draw.text((x, y), "Description:", color, font=font)

        font = ImageFont.truetype("Inter.ttf", size=40)
        content = str(response["weather"][0]["description"])
        color = "rgb(255, 255, 255)"
        (x, y) = (620, 430)
        draw.text((x, y), content, color, font=font)

        #temperature
        font = ImageFont.truetype("Inter.ttf", size=40)
        color = "rgb(0, 0, 0)"
        (x, y) = (135, 555)
        draw.text((x, y), "Current temperature: ", color, font=font)

        font = ImageFont.truetype("Inter.ttf", size=40)
        content = str(response["main"]["temp"]) + '\u00b0F'
        color = 'rgb(255, 255, 255)'
        (x, y) = (650, 555)
        draw.text((x, y), content, color, font=font)

        #feels like
        font = ImageFont.truetype("Inter.ttf", size=40)
        color = "rgb(0, 0, 0)"
        (x, y) = (135, 690)
        draw.text((x, y), "Feels like:", color, font=font)

        font = ImageFont.truetype("Inter.ttf", size=40)
        content = str(response["main"]["feels_like"]) + '\u00b0F'
        color = 'rgb(255, 255, 255)'
        (x, y) = (650, 690)
        draw.text((x, y), content, color, font=font)

        #humidity
        font = ImageFont.truetype("Inter.ttf", size=40)
        color = "rgb(0, 0, 0)"
        (x, y) = (135, 830)
        draw.text((x,y), "Humidity", color, font=font)

        font = ImageFont.truetype("Inter.ttf", size =40)
        content = str(response['main']['humidity']) + '%'
        color = 'rgb(255,255,255)'
        (x,y) = (650, 830)
        draw.text((x,y), content, color, font=font)

        #image.show()
        image.save("weather.png")
        embed=discord.Embed(title=f'Showing weather for {response["name"]}', color=discord.Color.blue())
        file = discord.File('weather.png')
        embed.set_image(url="attachment://weather.png")
        await ctx.send(embed=embed, file=file)



@bot.command()
async def magicball(ctx, *question):
    question_full = ' '.join(question)
    choices = ['It is certain.' ,
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
    response = random.choice(choices)
    embed=discord.Embed(title="The Magic Being, BotBot, has spoken!", timestamp=ctx.message.created_at, color=discord.Color.from_rgb(0,0,0))
    embed.add_field(name='Question: ', value=f'{question_full}', inline=True)
    embed.add_field(name='Answer: ', value=f'{response}', inline=False)
    file=discord.File('eightball.png')
    embed.set_thumbnail(url='attachment://eightball.png')
    await ctx.send(embed=embed, file=file)


@bot.command()
async def flip(ctx):
    answers = ['heads', 'tails']
    num = random.randint(0, 1)
    if(num == 0):
        await ctx.send(answers[0])
    else:
        await ctx.send(answers[1])




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
async def userinfo(ctx, *, user: discord.Member=None):
    date_format = "%a, %d %b %Y %I:%M %p"
    if user==None:
        user=ctx.author
    embed = discord.Embed(color=user.colour, description=user.mention, timestamp=ctx.message.created_at)
    embed.set_author(name=f"User Info - {user}")
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(user)+1) + f'/{len([m for m in ctx.guild.members])}')
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=True)
    embed.add_field(name='Status', value=f'{user.status}', inline=True)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Server permissions", value=perm_string, inline=False)
    embed.set_footer(text='USER ID: ' + str(user.id))
    await ctx.send(embed=embed)


@bot.command()
async def serverinfo(ctx):
    date_format = "%Y/%m/%d"
    description = str(ctx.guild.description)
    embed = discord.Embed(title=f'{ctx.guild.name} Server Information',description=description,color=ctx.guild.owner.color)
    embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
    embed.add_field(name="Owner", value=f'{ctx.guild.owner}', inline=True)
    embed.add_field(name="Channels", value=f'Text Channels: {len(ctx.guild.text_channels)}\n' f'Voice Channels: {len(ctx.guild.voice_channels)}', inline=True)
    print(ctx.guild.roles)
    embed.add_field(name="Roles", value=f'{len(ctx.guild.roles)}', inline=True)
    embed.add_field(name="Member Count", value=ctx.guild.member_count, inline=False)
    embed.set_footer(text=f'Server ID: {ctx.guild.id} • Created: {ctx.guild.created_at.strftime(date_format)}')
    await ctx.send(embed=embed)


@bot.command()
async def pfp(ctx, member: discord.Member=None):
    if member==None:
        member = ctx.author
    embed = discord.Embed(color=member.colour, description=f'Profile picture of {member.mention}')
    print(member.avatar_url)
    embed.set_image(url=f'{member.avatar_url}')
    await ctx.send(embed=embed)

@bot.command()
async def rps(ctx, message):
    answer = message.lower()
    choices =['rock', 'paper', 'scissors']
    bot_answer = random.choice(choices)
    print(bot_answer)
    if answer not in choices:
        await ctx.send('Please answer using rock, paper, scissors as input')
    else:
        if bot_answer == answer:
            await ctx.send(f'We got a tie. I also chose {answer}')
            await ctx.send('https://tenor.com/view/tom-and-jerry-jerry-the-mouse-jerry-shake-hands-handshake-gif-17827738')
        elif answer == 'rock':
            if bot_answer == 'paper':
                await ctx.send('I won. I chose paper to your rock.')
                await ctx.send('https://tenor.com/view/naruto-naruto-fortnite-naruto-l-fortnite-naruto-fortnite-dance-fortnite-dance-gif-23955255')
            else:
                await ctx.send('I lost. I chose scissors to your rock')
                await ctx.send('https://tenor.com/view/sad-cry-crying-tears-broken-gif-15062040')
        elif answer == 'scissors' or answer == 'scissor':
            if bot_answer == 'rock':
                await ctx.send('I won. I chose rock to your scissors.')
                await ctx.send('https://tenor.com/view/naruto-naruto-fortnite-naruto-l-fortnite-naruto-fortnite-dance-fortnite-dance-gif-23955255')
            else:
                await ctx.send('I lost. I chose paper to your scissors')
                await ctx.send('https://tenor.com/view/sad-cry-crying-tears-broken-gif-15062040')
        elif answer == 'paper':
            if bot_answer == 'rock':
                await ctx.send('I lost. I chose rock to your paper')
                await ctx.send('https://tenor.com/view/sad-cry-crying-tears-broken-gif-15062040')
            else:
                await ctx.send('I won. I chose scissor to your paper')
                await ctx.send('https://tenor.com/view/naruto-naruto-fortnite-naruto-l-fortnite-naruto-fortnite-dance-fortnite-dance-gif-23955255')


openai.api_key = os.getenv("OPENAI_API_KEY")
def chatBot(userInput):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Marvin is a chatbot that reluctantly answers questions with sarcastic responses\n\n You: How many pounds are in a kilogram?\n Marvin: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nMarvin: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarvin: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nMarvin: I’m not sure. I’ll ask my friend Google.\nYou:Whats up?\nMarvin: The direction, opposite the way gravity pulls\nYou:Do you live Java?\nMarvin: The tea or the programming language, I both hate them." + str(userInput) + "Marvin: ",
        temperature=0.5,
        max_tokens=500,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0.0)
    return response


@bot.command()
async def chat(ctx, *userinput):
    userText = ' '.join(userinput)
    print(userText)
    chatOutput = chatBot(userText)['choices'][0]['text']
    print(chatOutput)
    await ctx.send(chatOutput)



def studyNotes(userInput):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=str(userInput),
        temperature=0.3,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0)
    return response


@bot.command()
async def notes(ctx, *userinput):
    userText = ' '.join(userinput)
    chatOutput = chatBot(userText)['choices'][0]['text']
    print(chatOutput)
    await ctx.send(chatOutput)


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member=None, *, reason='No reason provided'):
    if member != None and member != ctx.author:
        await member.kick(reason=reason)
        embed=discord.Embed(title=f'{member} has been kicked from {ctx.guild.name}', color=discord.Color.red(), timestamp=ctx.message.created_at)
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)
        try:
            embed=discord.Embed(title=f'You have been kicked from {ctx.guild.name}', color=discord.Color.red(), timestamp=ctx.message.created_at)
            embed.add_field(name='Reason', value=reason)
            embed.set_footer(text=f'Kicked by {ctx.author}')
            await member.send(embed=embed)
        except:
            pass
    else:
        await ctx.send("Please mention a member or use their user ID to kick!")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permissions to kick this member!")
    else:
        raise error

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member=None, *, reason='No reason provided'):
    if member != None and member != ctx.author:
        await member.ban(reason=reason)
        embed=discord.Embed(title=f'{member} has been banned from {ctx.guild.name}', color=discord.Color.red(), timestamp=ctx.message.created_at)
        embed.add_field(name="Reason", value=reason)
        embed.set_footer(text=f'Banned by {ctx.author}')
        await ctx.send(embed=embed)
        try:
            embed=discord.Embed(title=f'You have been banned from {ctx.guild.name}', color=discord.Color.red(), timestamp=ctx.message.created_at)
            embed.add_field(name='Reason', value=reason)
            embed.set_footer(text=f'Banned by {ctx.author}')
            await member.send(embed=embed)
        except:
            pass
    else:
        await ctx.send("Please mention a member or use their user ID to kick!")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You don't have permissions to ban this member!")
    else:
        raise error

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, number: int=None):
    if number==None:
        await ctx.send("Please use a number from 1 or greater!")
    elif number==1:
        await ctx.channel.purge(limit=(number+1))
        embed=discord.Embed(title=f'Cleared 1 message', color=discord.Color.red(), timestamp=ctx.message.created_at)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
    elif number >1:
        await ctx.channel.purge(limit=(number+1))
        embed=discord.Embed(title=f'Cleared {number} messages', color=discord.Color.red(), timestamp=ctx.message.created_at)
        embed.set_footer(text=f'Requested by {ctx.author}')
        await ctx.send(embed=embed)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, BadArgument):
        await ctx.send('Please input a number!')
    elif isinstance(error, MissingPermissions):
        await ctx.send("You don't have permission to delete messages!")
    else:
        raise error

@bot.command()
async def password_gen(ctx):
    characters= string.ascii_letters + string.punctuation + string.digits
    password= "".join(random.choice(characters) for x in range(random.randint(8,16)))
    embed=discord.Embed(title='Password Generator', description=f"The generated password is: ||{password}||\nDon't share it with anybody else!", color=discord.Color.from_rgb(0,0,0), timestamp=ctx.message.created_at)
    embed.set_author(name='BotBot', icon_url=f'{bot.user.avatar_url}')
    file=discord.File('passwordicon.png')
    embed.set_thumbnail(url='attachment://passwordicon.png')
    await ctx.author.send(embed=embed, file=file)

@bot.command()
async def poll(ctx, question, *options):
    #def check(hours):
        #try:
            #int(hours)
            #is_int=True
       # except ValueError:
            #is_int=False
        #return hours.author == ctx.author and hours.channel == ctx.channel and is_int
    #hours= await bot.wait_for('message',check=check)
    if len(options) > 10:
        await ctx.send('Please only create 9 or less options!')
    else:
        embed=discord.Embed(title=f'{question}', color=ctx.message.author.color, timestamp=ctx.message.created_at)
        fields=[('Options','\n'.join([f"\n{numbers[idx]} {options[idx]}" for idx, option in enumerate(options)]))]
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
        message = await ctx.send(embed=embed)
        for idx, emoji in enumerate(options):
            await message.add_reaction(numbers[idx])
#@commands.command(pass_context=True)
#async def tally(self, ctx, id):
    #poll_message= await self.bot.get_message(ctx.message.channel, id)
    #if not poll_message.embeds:
        #return
    #embed=poll_message.embed[0]
    #if poll_message.author != ctx.message.server.me:
        #return


       # self.polls.append((message.channel.id, message.id))
        #self.bot.scheduler.addjob(self.complete_poll, "date", run_date=datetime.now()+timedelta(seconds=hours), args=[message.channel.id, message.id])

#async def complete_poll(self, channel_id, message_id):
    #message= await self.bot.get_channel(channel_id).fetch_message(message_id)
    #top_vote=max(message.reactions, key=lambda r: r.count)
    #await message.channel.send(f'{top_vote.emoji.name} was the most voted with {top_vote} votes!')

@bot.command()
async def deepfry(ctx):
    try:
        url=ctx.message.attachments[0].url
    except IndexError:
        print('Please send an attachment!')
        await ctx.send('Please send an attachment! I cannot do URLs currently')
    else:
        if url[0:26] == 'https://cdn.discordapp.com':
            imageName=str(uuid.uuid4()) + '.jpg'
            await ctx.message.attachments[0].save(imageName)
            print(imageName)
            img=Image.open(imageName)
            e = ImageEnhance.Sharpness(img)
            img = e.enhance(35)
            e = ImageEnhance.Contrast(img)
            img = e.enhance(2.3)
            e = ImageEnhance.Brightness(img)
            img = e.enhance(1.3)
            e = ImageEnhance.Color(img)
            img= e.enhance(5)
            temp = BytesIO()
            temp.name = 'deepfry.png'
            img.save(temp.name)
            embed = discord.Embed(title=f'Showing deepfry for {imageName}', color=discord.Color.blue())
            file = discord.File('deepfry.png')
            embed.set_image(url="attachment://deepfry.png")
            await ctx.message.reply(embed=embed, file=file)








youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    #'postprocessors': [{
        #'key': 'FFmpegExtractAudio',
        #'preferredcodec': 'mp3',
        #'preferredquality': '192',
    #}],
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


@bot.command(name='play', help='To play song')
async def play(ctx, url):
    if not 'https://' in url:
        await ctx.send('Please send a URL!')
        pass
    elif not commands.has_permissions(send_messages=True):
        await ctx.send('NOT AUTHORIZED!')
        return
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            print(filename)
            await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")
@play.error
async def play_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('Please include a URL! I cannot play music if there is no link!')
    else:
        raise error

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play command")


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    try:
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")
    except:
        await ctx.send('You are not in a voice channel!')

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")





def listToString(s):
    str1 = " \n"
    return str1.join(s)

bot.run(os.getenv('TOKEN'))