# bot.py
from keep_alive import keep_alive
 
import os
import random
import math

import discord
from discord.ext import commands
from dotenv import load_dotenv

from gtts import gTTS
from mutagen.mp3 import MP3
from db_modules import *
from blackjack import *
import asyncio

import youtube_dl

from joke_generator import generate

from dicts import *

currentPlaying = ""

langsDict = {v.lower(): k for k, v in langsDictOg.items()}

def audio_len(path):
    global MP3
    audio = MP3(path)
    return (audio.info.length)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(
    command_prefix=('yo ', ',','Yo '),
    description = "Custom bot developed by marco_jds and Phantomite for Memcraft",
    help_command = help_command
    )

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="memcraft 'yo help'"))
    print("Bot is ready!")

@bot.command(name='membot', help='Greet membot')
async def greet_bot(ctx):
    greetings = [
        'What\'s up '+str(ctx.author.name)+'?',
        'What\'s good '+str(ctx.author.name)+'?',
        'Yo '+str(ctx.author.name)+' musta?',
        'Yoooo '+str(ctx.author.name),
    ]

    response = random.choice(greetings)
    await ctx.send(response)
    if ctx.author.name=="deocs":
        await ctx.send("nako baka madisconnect ka nanaman")
    elif ctx.author.name=="Beans":
        await ctx.send("patambay condo")
    elif ctx.author.name=="Phantomite":
        await ctx.send("pasabi kay mina hi")
    elif ctx.author.name=="Not_Miguel":
        await ctx.send("who are u if youre not miguel")
    elif ctx.author.name=="jkkj3927":
        await ctx.send("hi jiniper")
    elif ctx.author.name=="robieboyy":
        await ctx.send("muda muda")
    elif ctx.author.name=="horanghae":
        await ctx.send(file=discord.File('janelle.jpg'))
    elif ctx.author.name=="marco_jds":
        await ctx.send(file=discord.File('lion.gif'))
    elif ctx.author.name=="lexsnts":
        await ctx.send(file=discord.File('cool.jpg'))
    elif ctx.author.name=="domimi":
        await ctx.send(file=discord.File('via.jpg'))
    elif ctx.author.name=="robieboyyy":
        await ctx.send(file=discord.File('rob.gif'))


@bot.command(name='tell me a joke', help='Tells a random joke', aliases=['joke', 'tell'])
async def joke(ctx):
    await ctx.send(generate())


@bot.command(name='say', help='Text-to-speech functionality', aliases=['tts'])
async def tts(ctx, language="", *, message=""):
    global gTTS

    if language=="" or language==None:
        await ctx.send("Say what?")
        return
    elif message=="":
        message=language

    try:
        speech = gTTS(text = message, lang = langsDict[str(language).lower()], slow = False)
        print("language found")
    except:
        speech = gTTS(text = message, lang = 'en', slow = False)
        message = str(language) + " " +message

    speech.save("audio.mp3")
    voicechannel = ctx.author.voice.channel
    try:
        vc = await voicechannel.connect()
    except:
        server = ctx.message.guild
        vc = server.voice_client
    vc.play(discord.FFmpegPCMAudio("audio.mp3"), after=lambda e: print("done"))
    counter = 0
    cwd = os.getcwd()
    duration = audio_len(cwd + "/audio.mp3")
    while not counter >= duration:
        await asyncio.sleep(1)
        counter +=1
    await vc.disconnect()

youtube_dl.utils.bug_reports_message = lambda: ''

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
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        # filename = data['title'] if stream else ytdl.prepare_filename(data)
        return data

@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{}, you're not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
    await ctx.send("Yo I'm here")

@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("Can't leave when i haven't joined")
    await ctx.send("See ya")

@bot.command(name='play', help='To play song', aliases=['p', 'pl'])
async def play(ctx,*,url=""):
    voice_client = ctx.message.guild.voice_client
    try:
        if voice_client.is_paused():
            voice_client.resume()
            await ctx.send("Resuming")
            return
    except:
        if not ctx.message.author.voice:
            await ctx.send("{}, you're not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()
    await ctx.send("Looking it up")

    if url != "":
        try :
            server = ctx.message.guild
            voice_channel = server.voice_client

            async with ctx.typing():
                with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
                    info = await YTDLSource.from_url(url, loop=bot.loop)
                    URL = info['formats'][0]['url']
                    await ctx.send('I gotchu, playing ***'+str(info['title'])+"***")
                voice_channel.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        except:
            await ctx.send("Exception here")

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    try:
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.pause()
            await ctx.send("Pausing")
        else:
            await ctx.send("Nothing is playing dude")
    except:
        await ctx.send("Nothing is playing dude")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    try:
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            voice_client.resume()
            await ctx.send("Resuming")
        else:
            await ctx.send("Nothing is playing dude")
    except:
        await ctx.send("Nothing is playing dude")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    try:
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Np, stopping")
        else:
            await ctx.send("Nothing is playing dude")
    except:
        await ctx.send("Nothing is playing dude")

@bot.command(name='lucky', help='Im Feeling Lucky', aliases=['Lucky', 'im feeling lucky', 'luck'])
async def lucky(ctx):
    if getBalance(ctx.author.name) < 20:
      await ctx.send("Your poor go work first")
    else:
        ticket = random.randint(1,100)
        target = random.randint(1,100)
        if ticket == target:
            await ctx.send("Congrats dude")
            price = getBalance("Ticket")
            addBalance(ctx.author.name, price)
            subtractBalance("Ticket",price)
            if getBalance("Ticket") == 0:
                addBalance("Ticket",2000)
        else:
            await ctx.send("Your number was "+str(ticket))
            await ctx.send("Lucky number was "+str(target))
            await ctx.send("Haha unlucky")
            subtractBalance(ctx.author.name, 20)
            addBalance("Ticket",20)
            await ctx.send("```The current prize is "+str(getBalance("Ticket"))+"```")

@bot.command(name='balance', help='Check Balance', aliases=['bal','acc','account'])
async def balance(ctx):
    if checkUser(ctx.author.name) == False:

      def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

      await ctx.send("Your current balance is " + str(getBalance(ctx.author.name)) + " answer the question right to add balance")

      Z = random.randint(6,10)
      Y = random.randint(1,5)
      x = Z-Y 
      await ctx.send("What is the value of X: X + Y = " + str(Z) + " when Y is = " + str(Y))
      
      msg = await bot.wait_for("message", check=check)

      if int(msg.content) == x:
        await ctx.send("Correct 200 was added to your account")
        addBalance(ctx.author.name, 200)
      else:
        await ctx.send(f"Nope it was {x}")
    
      Alex = random.randint(3,7)
      Steve = random.randint(1,5)
      left = (Alex) + math.floor(Alex/2) - 4
      await ctx.send("If Alex has " + str(Alex) + " chickens and gave Steve 4 chickens after feeding all the chicken wheat seeds, how many chickens does Alex still have?") 

      msg = await bot.wait_for("message", check=check)

      if int(msg.content) == left:
        await ctx.send("Correct 200 was added to your account")
        addBalance(ctx.author.name, 200)
        await ctx.send("Your current balance is " + str(getBalance(ctx.author.name)))
      else:
        await ctx.send(f"Nope it was {left}")
        await ctx.send("Your current balance is " + str(getBalance(ctx.author.name)))
    else:
      await ctx.send("Your current balance is " + str(getBalance(ctx.author.name)))


@bot.command(name='blackjack', help='Black Jack', aliases=['bj', '21'])
async def blackJack(ctx):
  def check(msg):
    return msg.author == ctx.author and msg.channel == ctx.channel 
  
  user = ctx.author.name

  await ctx.send("You currently have " + str(getBalance(user)))
  await ctx.send("How much do you bet ")
  
  bet = await bot.wait_for("message", check=check)

  subtractBalance(user, bet.content)
  
  await ctx.send ("Your bet is {} Your current balance is {}".format( bet.content,getBalance(user)))
  
  dealers_hand = generateHand(2)
  players_hand = generateHand(2)

  dealer = Player(dealers_hand)
  player = Player(players_hand)
  await ctx.send("Dealer has ? and " + str(dealers_hand[1]))
  await ctx.send("Dealers total so far = "+str(totalDict[dealer.cards[1].number]))
  await ctx.send("Player has "+str(players_hand).strip("[]"))
  await ctx.send("Your total ="+str(player.generateTotal()))

  while True:
    if checkPlayerBj(player) == True:
      await ctx.send("Congrats Blackjack!")
      addBalance(user, int(bet.content)*3)
      await ctx.send("You now have " + str(getBalance(user)))
      break

    await ctx.send ("Hit(h) or Stand(s)? ")

    a = await bot.wait_for("message", check=check)

    if a.content == "h":
      playerHit(player)
      await ctx.send("Player has "+str(players_hand).strip("[]"))
      await ctx.send("Your total = "+str(player.generateTotal()))
      if player.generateTotal() == 21 :
        a.content = "s"
      elif player.generateTotal() > 21:
        await ctx.send("\nPlayer loses, Dealer wins.")
        break


    if a.content == "s":
      await ctx.send("Player has "+str(players_hand).strip("[]"))
      await ctx.send("Your total ="+str(player.generateTotal()))

      if checkWin(player,dealer) == 1:
        await ctx.send("Dealer's Hand: "+str(dealer.cards).strip("[]"))
        await ctx.send("Dealer's Total: "+str(dealer.generateTotal()))    
        await ctx.send("\nPlayer Wins!")
        addBalance(user, int(bet.content)*2)
        await ctx.send("You now have " + str(getBalance(user)))
      
      elif checkWin(player,dealer) == 2:
        await ctx.send("Dealer's Hand: "+str(dealer.cards).strip("[]"))
        await ctx.send("Dealer's Total: "+str(dealer.generateTotal()))
        await ctx.send("\nPlayer loses, Dealer wins.")

      elif checkWin(player,dealer) == 3:
        await ctx.send("Dealer's Hand: "+str(dealer.cards).strip("[]"))
        await ctx.send("Dealer's Total: "+str(dealer.generateTotal()))
        await ctx.send("\nIts a Tie!")
        addBalance(user, bet.content)
        await ctx.send("You now have " + str(getBalance(user)))
      break 

keep_alive()
bot.run(TOKEN)