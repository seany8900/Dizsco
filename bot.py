#Using discord.py etc.
import discord, os
from discord.ext import commands, tasks
from discord.ext.commands import Bot, BadArgument, CommandNotFound, MissingRequiredArgument, NSFWChannelRequired
from discord import utils, Client
from discord.ext.commands import has_permissions, MissingPermissions
from traceback import format_exc
from discord import member, Intents, Guild
import time
import random
import asyncio
import json




#identifies prefix for commands
client = commands.Bot(command_prefix='?')
client.remove_command("help")

#declaring commands


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))   
    time.sleep(1)
    print('{0.user} is ready to do his job' .format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="?help"))



@client.event
#async def on_command_error(ctx, exc):
async def on_command_error(ctx, error):
    embed1 = discord.Embed(title="", desc="", colour=discord.Colour.blue())   
    embed1.add_field(name="⚠️Error⚠️", value=error)    
    await ctx.send(embed=embed1)     

@client.event
async def on_member_join(member):
    join = discord.Embed(description=f"Welcome to the server {member.name}", colour=discord.Colour.blue())
    join.set_thumbnail(url=f"{member.avatar_url}")

    join.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
    join.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
    
    channel = client.get_channel(id=765429164480004158)
    await ctx.channel.send(embed=join)

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
    #helpful_embed.add_field(name="join", value="makes the bot join the channel your in", inline=False)
    helpful_embed.add_field(name="pctips", value="gives you a good tip for your pc.", inline=False)
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
#Mod Cmds
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=": No reason has been provided"):
    print('Kick called for...')
    await member.kick(reason=reason)
    print('Kicking...')
    kicembed = discord.Embed(title="", desc="", colour=discord.Colour.blue())
    kicembed.add_field(name=f"Kicked {member.mention}", value=f"{member.mention} has been kicked for {reason}")
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


#@client.command()
#async def join(ctx):
    #channel = ctx.author.voice.channel
    #await channel.connect()

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
    
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)
    await ctx.send("messages deleted")
    
    
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
    ]
    await ctx.send(f'{random.choice(tips)}')


        


         


#runs bot
client.run('token')
