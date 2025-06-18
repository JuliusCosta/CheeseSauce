import random
import discord
# import time
import datetime
import threading
import asyncio
import sys
import os

intents = discord.Intents.all()
intents.members = True
# intents.GUILD_VOICE_STATES = True 
intents.message_content = True

client = discord.Client(intents=intents)

state = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    state['like_list'] = []
    state['dislike_list'] = []
    state['vc'] = False
    state['vcounter'] = 0
    state['haunting'] = False


@client.event
async def on_voice_state_update(member, before, after):
    if member == client.user and before.channel != None and after.channel == None:
        state['vcounter'] = 0
        state['vc'] = False
        state["haunting"] = False
    
    if member != client.user and after.channel != None and before.channel == None and state["haunting"] == False:
        if not state['vc']:
            state['vc'] = await after.channel.connect()
        state["haunting"] = True
        state['vcounter'] += 1

        while state["haunting"] is not False:
            sleepTime = random.randint(600, 1800)
            state["haunting"] = sleepTime
            await asyncio.sleep(sleepTime)
            if state["haunting"] != sleepTime:
                break
            
            randSound = random.choice(["scary2.mp3", "scary1.mp3", "fart.mp3", "money.mp3", "spooky1.mp3", "spookylaugh.mp3", "HotDamm.mp3"])
            state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source=("audiofiles/" + randSound)))

    if member != client.user and after.channel == None:
        # check who is left
        members = before.channel.members
        # if no one leave
        if len(members) == 1 and client.user in members:
            state['vcounter'] = 0
            await state['vc'].disconnect()
            state['vc'] = False
            state["haunting"] = False




@client.event
async def on_message(message):
    message_text = message.content.lower()
    if message.author == client.user:
        return
    
    rand = random.random()
    # print(rand)
    if rand < 0.00001:
        await message.channel.send('Bro is the ultimate banker')

    elif rand < 0.0001:
        await message.channel.send('Based')

    elif rand < 0.001:
        await message.channel.send('100% FACTS!')

    elif rand < 0.02:
        await message.channel.send('Do You?')

    if message.author.id in state['like_list'] and not 'sauce you are not cool' in message_text:
        await message.add_reaction('\N{HEAVY BLACK HEART}')
    
    if message.author.id in state['dislike_list'] and not 'sauce you are cool' in message_text:
        await message.add_reaction('\N{THUMBS DOWN SIGN}')
    

    if message_text.startswith('$hello'):
        await message.channel.send('Hello ' + message.author.display_name + "!")
    if 'cheese' in message_text:
        await message.channel.send('SAUCE!')
    if 'i bank nab' in message_text or 'i bank at nab' in message_text:
        await message.channel.send('Do You?')
    if 'drip' in message_text:
        await message.channel.send('SPLASH!')
    if 'sauce debug' in message_text:
        await message.channel.send('check terminal!')
        print(state)
    if 'quarters' in message_text:
        randInt = random.randrange(1,10)
        await message.channel.send(f'I\'ll take {randInt * 4} of those')
    if 'meow' in message_text:
        await message.channel.send('Meow :3')
        if message.author.voice is not None:
            state['vcounter'] = state['vcounter'] + 1  
            if not state['vc']:
                state['vc'] = await message.author.voice.channel.connect()
            state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/meow.mp3"))
            await asyncio.sleep(10)
            state['vcounter'] = state['vcounter'] - 1  
        if state['vcounter'] <= 0:
            state['vcounter'] = 0
            await state['vc'].disconnect()
            state['vc'] = False

    if 'release me' in message_text:
        await message.author.move_to(None)
    
    if 'kick me' in message_text:
        await message.channel.send('Bye ' + message.author.display_name)
        
        if not state['vc']:
            state['vc'] = await message.author.voice.channel.connect()
        state['vcounter'] = state['vcounter'] + 1  
        state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/circussong.mp3"))
        await asyncio.sleep(43)
        state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/ghostbanished.mp3"))
        await asyncio.sleep(4)
        await message.author.move_to(None)
        await asyncio.sleep(2)
        state['vcounter'] = state['vcounter'] - 1  
        if state['vcounter'] <= 0:
            state['vcounter'] = 0
            await state['vc'].disconnect()
            state['vc'] = False
    
    if 'sauce join call' in message_text:
        if message.author.voice is None:
            await message.channel.send('You arent in call')
        else:
            await message.channel.send('Lemme try')
            if not state['vc']:
                state['vc'] = await message.author.voice.channel.connect()
            state['vcounter'] = state['vcounter'] + 1  

    if 'sauce play' in message_text:
        await message.channel.send('Lets go gambling!!')
        state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/gamblecore.mp3"))
        await message.channel.send("done")
    if 'sauce leave call' in message_text:
        await message.channel.send('Goodbye')
        state['vcounter'] = 0
        await state['vc'].disconnect()
        state['vc'] = False
        state["haunting"] = False

    if 'sauce wait' in message_text:
        await message.channel.send("drip...")
        await asyncio.sleep(60)
        await message.channel.send("SPLASH!")
    
    if 'double' in message_text:
        message_list = message_text.split(" ")
        await message.channel.send(2 * int(message_list[1]))
    
    if 'sauce please' in message_text and 'more seconds' in message_text:
        message_list = message_text.split(" ")
        await message.channel.send("ok...")
        
        await asyncio.sleep(int(message_list[2]))
        state['vcounter'] = state['vcounter'] + 1  
        if not state['vc']:
            state['vc'] = await message.author.voice.channel.connect()
        await message.channel.send("begone")
        
        state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/evilclown.mp3"))
        await asyncio.sleep(8)
        await message.author.move_to(None)
        await asyncio.sleep(2)
        state['vcounter'] = state['vcounter'] - 1  
        if state['vcounter'] <= 0:
            state['vcounter'] = 0
            await state['vc'].disconnect()
            state['vc'] = False

    if 'sauce terrible stream' in message_text:
        # await message.channel.send("ok...")
        state['vcounter'] = state['vcounter'] + 1  
        if not state['vc']:
            state['vc'] = await message.author.voice.channel.connect()
        state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/crushskull.mp3"))
        await asyncio.sleep(3)
        await message.author.move_to(None)
        await asyncio.sleep(1)
        state['vcounter'] = state['vcounter'] - 1  
        if state['vcounter'] <= 0:
            state['vcounter'] = 0
            await state['vc'].disconnect()
            state['vc'] = False

    if 'banish me' in message_text:
        await message.channel.send("ok...")
        state['vcounter'] = state['vcounter'] + 1  
        if not state['vc']:
            state['vc'] = await message.author.voice.channel.connect()
        state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/ghostbanished.mp3"))
        await asyncio.sleep(4)
        await message.author.move_to(None)
        await asyncio.sleep(1)
        state['vcounter'] = state['vcounter'] - 1  
        if state['vcounter'] <= 0:
            state['vcounter'] = 0
            await state['vc'].disconnect()
            state['vc'] = False

    if 'mute me' in message_text:
        await message.author.edit(mute=True)

    if 'who is here' in message_text:
        members = message.author.voice.channel.members
        response = ""
        for member in members:
            response += member.display_name + "\n"
        await message.channel.send(response)

    if 'talking stick on' in message_text:
        members = message.author.voice.channel.members
        state['vcounter'] = state['vcounter'] + 1
        if not state['vc']:
            state['vc'] = await message.author.voice.channel.connect()
        state["stick_members"] = members
        state["stick"] = True
        for member in members:
            await member.edit(mute=True)
        while state["stick"]:
            for member in members:
                state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/beep-101soundboards.mp3"))
                await member.edit(mute=False)
                await asyncio.sleep(5)
                if state["stick"]:
                    await member.edit(mute=True)
        
    
    if 'talking stick off' in message_text:
        state["stick"] = False
        for member in state["stick_members"]:
            await member.edit(mute=False)
        state['vcounter'] = state['vcounter'] - 1  
        if state['vcounter'] <= 0:
            state['vcounter'] = 0
            await state['vc'].disconnect()
            state['vc'] = False

    if 'fire' in message_text:
        await message.add_reaction('\N{FIRE}')
    
    if 'bank' in message_text or 'money' in message_text:
        await message.add_reaction('\N{MONEY BAG}')
        await message.add_reaction('\N{HEAVY DOLLAR SIGN}')
        await message.add_reaction('\N{MONEY-MOUTH FACE}')

    if 'sauce you are cool' in message_text:
        await message.channel.send("thanks")
        state['like_list'].append(message.author.id)
        state['dislike_list'].remove(message.author.id)

    if 'sauce you are not cool' in message_text:
        await message.channel.send("bruh")
        state['dislike_list'].append(message.author.id)
        state['like_list'].remove(message.author.id)

    if 'sauce you are ok' in message_text:
        await message.channel.send("ok")
        if message.author.id in state['dislike_list']:
            state['dislike_list'].remove(message.author.id)
        if message.author.id in state['like_list']:
            state['like_list'].remove(message.author.id)
    
    if 'what is time' in message_text:
        rn = str(datetime.datetime.now().time())
        await message.channel.send(rn)

    if 'sauce are you in call' in message_text:
        if(state["vc"]):
            await message.channel.send("yes")
        else:
            await message.channel.send("no")
        
    
    if 'tell me when its ' in message_text:
        now = datetime.datetime.now()
        asked_time = message_text.split('tell me when its ')[1]
        split_time = asked_time.split(':')
        hours, minutes, seconds =  split_time[0], split_time[1], split_time[2]
        alarm_time = datetime.datetime.combine(now.date(), datetime.time(int(hours), int(minutes), int(seconds)))
        await asyncio.sleep((alarm_time - now).total_seconds())
        await message.channel.send("now")

    if 'sauce kick me at ' in message_text:
        await message.channel.send("ok...")
        now = datetime.datetime.now()
        asked_time = message_text.split('sauce kick me at ')[1]
        split_time = asked_time.split(':')
        hours, minutes, seconds =  split_time[0], split_time[1], split_time[2]
        alarm_time = datetime.datetime.combine(now.date(), datetime.time(int(hours), int(minutes), int(seconds)))
        secondstill = (alarm_time - now).total_seconds()
        if secondstill < 0:
            secondstill += 86400
        await asyncio.sleep(secondstill)
        
        state['vcounter'] = state['vcounter'] + 1  
        if not state['vc']:
            state['vc'] = await message.author.voice.channel.connect()
        state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/circussong.mp3"))
        await asyncio.sleep(43)
        state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/ghostbanished.mp3"))
        await asyncio.sleep(4)
        await message.author.move_to(None)
        await asyncio.sleep(2)
        state['vcounter'] = state['vcounter'] - 1  
        if state['vcounter'] <= 0:
            state['vcounter'] = 0
            await state['vc'].disconnect()
            state['vc'] = False

    if 'how long till ' in message_text:
        now = datetime.datetime.now()
        asked_time = message_text.split('how long till ')[1]
        split_time = asked_time.split(':')
        hours, minutes, seconds =  split_time[0], split_time[1], split_time[2]
        alarm_time = datetime.datetime.combine(now.date(), datetime.time(int(hours), int(minutes), int(seconds)))
        secondstill = (alarm_time - now).total_seconds()
        if secondstill < 0:
            secondstill += 86400
        await message.channel.send(secondstill)

    # intervals chance growing chance
    if 'sauce lets go gambling' in message_text:
        variables = message_text.split('sauce lets go gambling ')[1]
        variable_list = variables.split(' ')
        quiet = bool(variable_list[0].startswith("q"))
        interval = int(variable_list[1])
        chance = float(variable_list[2])
        growth = 0
        if len(variable_list) >= 4:
            growth = float(variable_list[3])

        lives = 1
        if len(variable_list) == 5:
            lives = int(variable_list[4])

         
        if not state['vc']:
            state['vc'] = await message.author.voice.channel.connect()
        state['vcounter'] = state['vcounter'] + 1 

        if quiet:
            state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/startupbeeps.mp3"))
            await asyncio.sleep(1)
        else:
            state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/letsgogambling.mp3"))
            await asyncio.sleep(2)
        # going = True
        while lives > 0:
            await asyncio.sleep(interval)
            rand = random.random()
            # print(message.author.display_name)
            # print(rand)
            # print(chance)
            if rand < chance:
                lives -= 1
                if quiet:
                    state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/badbeep.mp3"))
                    await asyncio.sleep(2)
                else:
                    state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/awdangit.mp3"))
                    await asyncio.sleep(2)
                if lives > 1:
                    await message.channel.send(str(lives) + " lives left")
                elif lives == 1:
                    await message.channel.send("I\'m just about done with you")
            else:
                if quiet:
                    state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/winbeep.mp3"))
                    await asyncio.sleep(1)
                else:
                    state['vc'].play(discord.FFmpegPCMAudio(executable=ffmpeg_location, source="audiofiles/icantstopwinning.mp3"))
                    await asyncio.sleep(2)
            chance += growth
        
        await message.author.move_to(None)
        state['vcounter'] = state['vcounter'] - 1  
        if state['vcounter'] <= 0:
            state['vcounter'] = 0
            await state['vc'].disconnect()
            state['vc'] = False
        

    
    if 'sauce help' in message_text:
        response = """
'$hello' -> i say hi back
'cheese' -> SAUCE!!
'drip' -> SPLASH!!
'quarters' -> ill take some of those
'meow' -> i respond, also if youre in call i play a part of Hello Gaby by NMIXX
'release me' -> bye bye no music
'kick me' -> i kick you while playing funny music
'sauce join call' -> i arrive
'sauce play' -> LETS GO GAMBLING
'sauce leave call' -> i depart
'sauce wait' -> drip SPLASH with build up
'double X' -> doubles X
'sauce please X more seconds' -> i wait and then kick you with evil clown music (it kinda goes hard)
'banish me' -> youve been banished
'who is here' -> i tell you who you are talking to
'mute me' -> i server mute you if you dont have admin you can unmute yourself with the following two commands
'talking stick on' -> everyone is muted and only gets 5 second turns to talk marked with a beep
'talking stick off' -> i unmute everyone
'fire' -> sick dude
'bank' -> cha-ching
'sauce you are cool' -> i like you
'sauce you are not cool' -> i dislike you
'sauce you are ok' -> we chill
'what is time' -> i tell you the time again? why are there two?
'tell me when its H:M:S' -> i send a message at your asked for time
'sauce kick me at H:M:S' -> i kick you at that time with circus music and banishment
'how long till H:M:S' -> i tell you how many seconds until the asked for time
'sauce lets go gambling q/l I P G L' -> gambles how much longer you will stay in call q/l is whether its loud or quiet, I is interval in seconds between rolls, P is probability of kicking you each roll (1 = 100%, 0.5 = 50%), G is growth of the chance to kick you and can be left out and can be 0, L is lives can be left out and will be set to 1 needs growth declared  
'sauce help' -> brings this up (duh)
        """
        await message.channel.send(response)

token=None
ffmpeg_location="C:/ffmpeg/bin/ffmpeg"

args = sys.argv
# if len(args) >= 2:
#     token = args[1]
if len(args) >= 2:
    ffmpeg_location = args[1]
if os.environ["CHEESE_SAUCE_TOKEN"]:
    token = os.environ["CHEESE_SAUCE_TOKEN"]

client.run(token)
