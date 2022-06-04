import time
from datetime import date
import discord
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
import requests
import random
from jikanpy import Jikan
import numpy as np
import os
import openai
from PIL import Image, ImageFont, ImageDraw




intents = discord.Intents.default()
intents.members = True
load_dotenv()
bot = commands.Bot(command_prefix='+', intents=intents, activity=discord.Activity(type=discord.ActivityType.listening, name="+help"))


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
        await ctx.send("The main weather is: " + response["weather"][0]["main"] + '\n' +
                       "Description: " + response["weather"][0]["description"] + '\n' +
                       "The current temperature is " + str(response["main"]["temp"]) + '\u00b0F\n' +
                       "Feels like " + str(response["main"]["feels_like"]) + "\u00b0F")

        image = Image.open("post.png")
        draw = ImageDraw.Draw(image)
        #title and subheading
        font = ImageFont.truetype("Inter.ttf", size=50)
        content = "Latest Weather Forecast for " + city_full
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

        image.show()
        image.save("weather.png")
        await ctx.send(file=discord.File('weather.png'))














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
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=True)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='USER ID: ' + str(user.id))
    await ctx.send(embed=embed)


@bot.command()
async def serverinfo(ctx):
    date_format = "%a, %d %b %Y %I:%M %p"
    description = str(ctx.guild.description)
    embed = discord.Embed(title=f'{ctx.guild.name} Server Information',description=description,color=ctx.guild.owner.color)
    embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
    embed.add_field(name="Owner", value=f'{ctx.guild.owner}', inline=True)
    embed.add_field(name="Channels", value=f'Text Channels: {len(ctx.guild.text_channels)}\n' f'Voice Channels: {len(ctx.guild.voice_channels)}', inline=True)
    print(ctx.guild.roles)
    embed.add_field(name="Roles", value=f'{len(ctx.guild.roles)}', inline=True)
    embed.add_field(name="Member Count", value=ctx.guild.member_count, inline=False)
    embed.set_footer(text=f'Server ID: {ctx.guild.id}  Created: {ctx.guild.created_at.strftime(date_format)}')
    await ctx.send(embed=embed)


@bot.command()
async def pfp(ctx, member: discord.Member=None):
    if member==None:
        member = ctx.author
    embed = discord.Embed(color=member.colour, description=f'Profile picture of {member.mention}')
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
        prompt="Marvin is a chatbot that reluctantly answers questions with sarcastic responses\n\n You: How many pounds are in a kilogram?\n Marvin: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nMarvin: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nMarvin: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou: What is the meaning of life?\nMarvin: I’m not sure. I’ll ask my friend Google.\n" + str(userInput) + "Marvin: ",
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










def listToString(s):
    str1 = " \n"
    return str1.join(s)

bot.run(os.getenv('TOKEN'))

