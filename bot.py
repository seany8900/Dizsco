#Using discord.py etc.
import discord, os
from discord.ext import commands, tasks
from discord.ext.commands import Bot, BadArgument, CommandNotFound, MissingRequiredArgument, NSFWChannelRequired
from discord import utils, Client
from discord.ext.commands import has_permissions, MissingPermissions
from traceback import format_exc
from discord import member, Intents, Guild
from discord.utils import get
import time
import random
import asyncio
import json
import re



#custom prefixes
def get_prefix(client, message):
    with open('prefixes.json', 'r')as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


#identifies prefix for commands
client = commands.Bot(command_prefix= get_prefix)
client.remove_command("help")













#nono words

with open('swearWords.txt', 'r') as file:
    swears = file.read().strip().lower().split(', ')





#declaring commands


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))   
    time.sleep(1)
    print('{0.user} is ready to do his job' .format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="?help"))


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r')as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '?'

    with open('prefixes.json', 'w')as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r')as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w')as f:
        json.dump(prefixes, f, indent=4)



@client.event
#async def on_command_error(ctx, exc):
async def on_command_error(ctx, error):
    embed1 = discord.Embed(title="", desc="", colour=discord.Colour.blue())   
    embed1.add_field(name="⚠️Error⚠️", value=error)    
    await ctx.send(embed=embed1)     


@client.event 
async def on_message(message):
    
        
    if any(swears in message.content.strip().lower() for swears in swears):
           
        await message.delete()
        await message.channel.send(f"{message.author.mention}, don't say that word")
        await client.process_commands(message)
    else:
            await client.process_commands(message)








@client.event
async def on_member_join(member):
    join = discord.Embed(description=f"Welcome to the server {member.mention}", colour=discord.Colour.blue())
    join.set_thumbnail(url=f"{member.avatar_url}")

    join.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
    join.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
    channel = discord.utils.get(member.guild.channels, name='general')
    
    await channel.send(embed=join)








@client.command()
async def help(ctx):
    helpful_embed = discord.Embed(title="Commands", description="This is a list of commands", colour=discord.Colour.blue())
    helpful_embed.add_field(name="help", value="Shows this message", inline=False)
    helpful_embed.add_field(name="test", value="tests if the bot is working", inline=False)
    helpful_embed.add_field(name="oreos", value="when your mom buys you oreos", inline=False)
    helpful_embed.add_field(name="oreosforever", value="sends oreos 999 times", inline=False)
    helpful_embed.add_field(name="say", value="repeats what you say after the command", inline=False)
    helpful_embed.add_field(name="spam", value="spams @ everyone", inline=False)
    helpful_embed.add_field(name="modcmds", value="Shows a list of commands for Mods/Admins", inline=False)
    helpful_embed.add_field(name="join", value="makes the bot join the voice channel your in", inline=False)
    helpful_embed.add_field(name="leave", value="makes the bot leave the voice channel your in", inline=False)
    helpful_embed.add_field(name="pctips", value="gives you a good tip for your pc.", inline=False)
    helpful_embed.add_field(name="meme", value="sends a bad meme", inline=False)
    await ctx.send(embed=helpful_embed)


@client.command()
async def test(ctx, *, content='Tests the bot and its ping'):
    embed = discord.Embed(title="", colour=discord.Colour.blue())
    embed.add_field(name="⚠️Test⚠️", value=f"If you see this message I am working. My ping is {round(client.latency * 1000)}ms")
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_messages=True)
async def modcmds(ctx):
    cmds = discord.Embed(title="Mod/Admin commands", desc="Commands only Mods/Admins can use", colour=discord.Colour.blue())
    cmds.add_field(name="prefix", value="changes the prefix", inline=False)
    cmds.add_field(name="prefix example", value="```?prefix [new_prefix]```", inline=False)
    cmds.add_field(name="ban", value="bans a user from the guild", inline=False)
    cmds.add_field(name="ban example", value="```?ban [user] [reason]```", inline=False)
    cmds.add_field(name="unban", value="unbans a user from the guild", inline=False)
    cmds.add_field(name="unban example", value="```?unban [username]#[usernumber]```", inline=False)
    cmds.add_field(name="kick", value="kicks a user from the guild", inline=False)
    cmds.add_field(name="kick example", value="```?kick [user] [reason]```", inline=False)
    cmds.add_field(name="mute", value="gives the member the 'muted' role", inline=False)
    cmds.add_field(name="mute example", value="```?mute [user] [reason]```", inline=False)
    cmds.add_field(name="unmute", value="takes the 'muted' role away", inline=False)
    cmds.add_field(name="unmute example", value="```?unmute [user]```", inline=False)
    cmds.add_field(name="clear", value="clears certain amount of messages", inline=False)
    cmds.add_field(name="clear example", value="```?clear [integer]```", inline=False)
    cmds.add_field(name="rules", value="like the ?say cmd but it is embeded with the title **Rules**. Useful for the rules channel.", inline=False)
    cmds.add_field(name="rules example", value="```?rules [rule number] [rule description] continue...```", inline=False)
    await ctx.message.delete()
    await ctx.author.send(embed=cmds)


@client.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, prefix):
    with open('prefixes.json', 'r')as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w')as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f'⚠️Prefix changed to: `{prefix}`⚠️')




@client.command(name="hi" aliases=["he
async def prefix(ctx, prefix):
   await ctx.send(f"Hello {ctx.author.mention}! My name is Dizsco I can do lots of things! Do {prefix}help to see what I can do. If you have any problems contact my creator seany#6969")                      



#Mod Cmds
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=": No reason has been provided"):
    print('Kick called for...')
    await member.kick(reason=reason)
    print('Kicking...')
    kicembed = discord.Embed(title="", desc="", colour=discord.Colour.blue())
    kicembed.add_field(name=f"Kicked {member}", value=f"{member.mention} has been kicked for {reason}")
    print('Member kicked')
    await ctx.send(embed=kicembed)



@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=": No reason has been provided"):
    print('Ban called for...')
    await member.ban(reason=reason)
    print('Banning...')
    banembed = discord.Embed(title="", desc="", colour=discord.Colour.blue())
    banembed.add_field(name=f"Banned {member.name}", value=f"{member.name} has been banned for {reason}" )
    print('Member banned')
    await ctx.send(embed=banembed)



@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    embed = discord.Embed(title='', description='', colour = discord.Colour.blue())
    embed.add_field(name='User unbanned', value=f'{member} has been unbanned')
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(embed=embed)
            return


@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member : discord.Member=None, reason=": No reason has been provided"):
    role = discord.utils.get(ctx.guild.roles, name = "muted")
    await member.add_roles(role)
    muted = discord.Embed(title=f"{member.name} has been muted", description=f"{member.mention} has been muted for {reason}", colour=discord.Colour.blue())
    await ctx.message.delete()
    await ctx.send(embed=muted)


@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()



@client.command()
async def leave(ctx):  
    await ctx.voice_client.disconnect()


    
        

    
     



    
    
    

@client.command()
@commands.has_permissions(administrator=True)
async def rules(ctx, *, arg):
    embed = discord.Embed(title='Rules', description=arg, colour=discord.Colour.blue())
    await ctx.message.delete()
    await ctx.send(embed=embed)






@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member : discord.Member=None):
    
    unmute = discord.Embed(title=f"{member.name} has been unmuted", description=f"{member.mention}, you have been unmuted", colour=discord.Colour.blue())
    role = discord.utils.get(ctx.guild.roles, name="muted")
    await member.remove_roles(role)
    await ctx.message.delete()
    await ctx.send(embed=unmute)




@client.command()
@commands.is_nsfw()
async def oreosforever(ctx):
    for i in range(999):
        await ctx.send('https://cdn.discordapp.com/attachments/724511749516165211/756566771716194454/oreos.mov')



@client.command()
@commands.is_nsfw()
async def oreos(ctx):
    for i in range(5):
        await ctx.send('https://cdn.discordapp.com/attachments/724511749516165211/756566771716194454/oreos.mov')
    


@client.command()
async def say(ctx, *, arg):
    await ctx.message.delete()
    await ctx.send(arg)

    


    
    
@client.command()
@commands.has_permissions(manage_messages=True)
async def spam(ctx):
    for i in range(100):
        await ctx.send('@everyone')


@client.command(name="clear", aliases=["purge"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, limit: int ):
    
  
    await ctx.channel.purge(limit=limit + 1)
    await ctx.send(f"⚠️`{limit} messages` have been deleted⚠️")
    time.sleep(3)
    await ctx.channel.purge(limit= 1)
    
    
@client.command()
async def pctips(ctx):
    
    
    tips = [
        '**Malwarebytes**. Malwarebytes is a good free secondary scanner. If you have a free premium trial of malwarebytes be sure to turn off realtime features if your using another AV. https://www.malwarebytes.com/mwb-download/',
        '**CCleaner**. CCleaner is a good free tool to have in hand. It gets rid of uneccesary and temporary files that are uneeded. Good if you want to clear some space or speed up that potato of yours. https://www.ccleaner.com/ccleaner/download',
        '**Opera GX**. Opera GX is a decent web browser made by Opera. It has built in adblock and vpn. Its basically a browser for *gamers*. https://www.opera.com/gx',
        "**IP Grabbers**. https://grabify.link/U7JW67 don't click on that link. That link is known as an IP grabber. The person who sends it to you can see your IP and a rough estimate of your location if you click on it. Thats why VPNs are good. Be careful when clicking on links from strangers!",
        "**Anti-Virus**. Have you ever heard someone say *brain.exe is all I need* or *windows defender is good enough*. While they can be true even being smart on the internet can very rarely keep you virus free and Windows Defender takes a lot of configuration to make it good. If you want a good **FREE** AntiVirus I recommend https://www.bitdefender.com/solutions/free.html or https://usa.kaspersky.com/free-antivirus",
        '**Adblocking**. I think having an Adblock is very important. Have you ever been trying to install minecraft mods and you see a fake download button? That is a very good way to get a virus. Thats why having an adblock is very helpful not only can it stop annoying ads on youtube and twitch but it also can protect you from *malvertising*. https://chrome.google.com/webstore/detail/adblock-%E2%80%94-best-ad-blocker/gighmmpiobklfepjocnamgkkbiglidom',
        '**VirusTotal**. Have you ever downloaded something and it seems sketchy, like *Free Among Us* or *Roblox hacks*? Well fear no more because with VirusTotal you can scan sketchy links and files with multiple AntiVirus engines *for free*. Some things can be *false positives* though so be sure to look at the user rating too. https://www.virustotal.com/gui/',
        '**Sorry I had to**. https://youtu.be/rSvBFm_MuXw'
    ]
    await ctx.send(f'{random.choice(tips)}')


@client.command()
async def meme(ctx):
    memes = [
        'https://cdn.discordapp.com/attachments/765429164480004158/768251989687271474/video0.mp4',
        'https://cdn.discordapp.com/attachments/765429164480004158/768251205637505054/video1.mp4',
        'https://cdn.discordapp.com/attachments/765429164480004158/768251204777279488/video0.mov',
        'https://cdn.discordapp.com/attachments/765429164480004158/768251201497071616/video0.mp4',
        'https://cdn.discordapp.com/attachments/765429164480004158/768252738126741535/video0_1.mp4',
        'https://cdn.discordapp.com/attachments/765429164480004158/768252988006334494/mmm.jpg',
        'https://cdn.discordapp.com/attachments/765429164480004158/768253300679639060/Eh2WsS4VoAA-gp6.png',
        'https://cdn.discordapp.com/attachments/754761389700284438/767905418747314206/video0.mov',
        'https://cdn.discordapp.com/attachments/754761389700284438/767904223328600074/bradenjames__20201019_171704_0.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/767903967866650644/video0.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/767834201872793610/discord._.chan_20201016_103802_0.mp4',  
        'https://cdn.discordapp.com/attachments/754761389700284438/767900546048458762/video0.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/765715209787539486/video0.mov',
        'https://cdn.discordapp.com/attachments/754761389700284438/765714722178859048/video0.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/765712847426289704/yiff.yaff.snorff_20201013_160920_0.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/765713146132168764/itssarthurr.__20201013_161031_0.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/765711249706713178/video0.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/765708484678516756/video0.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/765708363299815424/video0.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/765707359796330497/video0.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/765706670079737886/nochillrick_20201012_211150_0.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/765706551075405834/video0.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/765706144852607006/video0.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/765703773732995082/reelpods_20201012_175402_0.mp4',
        'https://cdn.discordapp.com/attachments/722559237896536136/765318597022056448/I_give_you_fire_you_give_me_rock.mp4',
        'https://cdn.discordapp.com/attachments/754761389700284438/765376178412191745/wholesomememesforalluwu_20201012_175130_0.mp4',
        'https://cdn.discordapp.com/attachments/681580967877410845/768557919980748810/image8.png',
        'https://cdn.discordapp.com/attachments/681580967877410845/768557919171772456/image5.png',
        'https://cdn.discordapp.com/attachments/681580967877410845/768557917959618596/image2.png',
        'https://cdn.discordapp.com/attachments/681580967877410845/768557917280010280/image0.png',
        'https://cdn.discordapp.com/attachments/681580967877410845/768557706713497630/image7.png',
        'https://cdn.discordapp.com/attachments/681580967877410845/768557705907929118/image4.jpg',
        'https://cdn.discordapp.com/attachments/681580967877410845/768557704339390474/image0.png',
        'https://cdn.discordapp.com/attachments/755257724547366935/768560747197366322/video0-1.mp4',
        'https://cdn.discordapp.com/attachments/755257724547366935/768562591206735973/video0.mp4',
        'https://cdn.discordapp.com/attachments/755257724547366935/768562620415868946/video0.mp4',
        'https://cdn.discordapp.com/attachments/755257724547366935/768562831787950080/video0.mp4',
        'https://cdn.discordapp.com/attachments/755257724547366935/768563000508153917/video0.mp4',
        'https://cdn.discordapp.com/attachments/755257724547366935/768563615716212776/video0.mp4',
        'https://cdn.discordapp.com/attachments/755257724547366935/768565480335343656/video0.mp4 , https://cdn.discordapp.com/attachments/755257724547366935/768565480604303390/video1.mp4',
        'https://cdn.discordapp.com/attachments/755257724547366935/768567446835429406/video0-1.mov',
        'https://cdn.discordapp.com/attachments/754761389700284438/768253045028945930/video0.mp4',
        'https://cdn.discordapp.com/attachments/702687635579338762/766179182559756288/video0.mp4',
        'https://cdn.discordapp.com/attachments/702687635579338762/763425790380736512/GANGSTAARRRRRRRRR.mp4',
        'https://cdn.discordapp.com/attachments/702687635579338762/753658326956507156/video0_4.mp4',
        'https://www.youtube.com/watch?v=blgvslrfYV8&ab_channel=surrealentertainment',
        'https://cdn.discordapp.com/attachments/702687635579338762/749196743610204160/Redacted-4.mp4',
        'https://cdn.discordapp.com/attachments/702687635579338762/748554094800666684/g.mp4',
        'https://cdn.discordapp.com/attachments/702687635579338762/748483608020385872/cat_fade-1.mp4',
        'https://www.youtube.com/watch?v=IdoD2147Fik',
        'https://cdn.discordapp.com/attachments/702687635579338762/748444251498479677/video0.mp4',
        'https://cdn.discordapp.com/attachments/742761953973502023/744294341375164466/video0.mp4',
        'https://cdn.discordapp.com/attachments/746547171645587608/746932785935024242/Hot_anime_girls_1.mp4',
        'https://cdn.discordapp.com/attachments/702687635579338762/746430420157202563/video0.mov',
        'https://cdn.discordapp.com/attachments/742776979119407135/743248903851212891/video0.mp4',
        'https://youtu.be/p5L9-k0uV2A',
        'https://www.youtube.com/watch?v=3KxEp9DURCc',
        'https://cdn.discordapp.com/attachments/702687635579338762/739216403651100713/video7.mp4',
    ]
    await ctx.send(f'{random.choice(memes)}')

         


#runs bot
client.run('token goes here')
