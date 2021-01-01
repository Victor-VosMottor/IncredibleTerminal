import asyncio
import math
import random
import re

import discord
from discord.ext import commands
from discord.ext.tasks import loop
from discord.utils import get
from sympy import sympify
import requests
import urbandict
import wikipedia

import os

settings = {
    'token': os.environ['TOKEN'],
    'bot': '@IncredibleTerminal',
    'id': 792055705795952690,
    'prefix': '!!'  # '!!'
}

bot = commands.Bot(command_prefix=settings['prefix'])
client = discord.Client()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content
    author = message.author

    if author != 'IncredibleTerminal#3897':
        await send(f'Message "{msg}" was posted by {message.author}', 792779854621442088)

    if msg.startswith('!flag:'):
        await message.delete()
        await send(f'New flag: {msg}', 794592687181398056)

    elif msg.startswith('!modmsg:'):
        await message.delete()
        await send(f'New mod-message: {msg}', 794592687181398056)

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    await send(f'A new member has joined the server: {member}', 792779854621442088)

@bot.event
async def on_member_remove(member):
    await send(f'A new member has left the server: {member}', 792779854621442088)

@bot.event
async def on_message_delete(message):
    await send(f'"{message.content}" by {message.author} was deleted.', 792779854621442088)

@bot.event
async def on_message_edit(before, after):
    await send(f'"{before.content}" by {before.author} was changed to "{after.content}"', 792779854621442088)


async def send_msg(channel_id, msg):
    channel = bot.get_channel(channel_id)
    await channel.send(msg)

async def send(what, where):
    asyncio.run_coroutine_threadsafe(send_msg(where, what), bot.loop)



@bot.command(name='chk-channel')
async def _chk(ctx):
    await ctx.send(ctx.channel.id)

@bot.command(help='checks whether is bot running or not')
async def alive(ctx):
    await ctx.send(random.choice(['Beep boop. Yeah.', 'Of course... Why do you ask BTW?', 'Yup.']))

@bot.command(help='print, echo, console.log, writeln, println')
async def echo(ctx, arg):
    await ctx.send(arg)

@bot.command(help="evaluates a math expression")
async def calc(ctx, *what_to_calc):
    try:
        await ctx.send(sympify(' '.join(what_to_calc), locals={'PI': math.pi, 'E': math.e}).evalf(15))
    except:
        await ctx.send(sympify(' '.join(what_to_calc), locals={'PI': math.pi, 'E': math.e}))

@bot.command(pass_context=True)
@commands.has_role('VosMottor')
async def kick(ctx, user: discord.Member):
    await ctx.send(f'The Kicking Hammer has awoken! {user.name} has been banished')
    await ctx.guild.kick(user)

@bot.command(help='creates new channel')
async def addroom(ctx, name):
    guild = ctx.message.guild
    await guild.create_text_channel(name)

@bot.command(pass_context=True)
@commands.has_role('VosMottor')
async def ban(ctx, user: discord.Member):
    await ctx.send(f'The Ban Hammer has awoken! {user.name} has been banished')
    await ctx.guild.ban(user)

@bot.command(pass_context=True, name='ur-ban-dict', description='looks up in urban disctionary')
async def lookup(ctx, word):
    dfns = urbandict.define(word)
    definition = '\n'.join(f'```\n{dfn["word"]}\nDefinition: {dfn["def"]}\nExample: {dfn["example"]}```' for dfn in dfns)
    embed = discord.Embed(title=word,
                          description=definition,
                          color=discord.Color.blue())
    await ctx.send(embed=embed)

@bot.command(pass_context=True, help='gives user a role', name='give-role')
@commands.has_role("VosMottor")
async def adduser(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)


@bot.command(pass_context=True, name='wikipedia', description='looks up in Wikipedia')
async def _wikipedia(ctx, word, lang=None):
    print(word)
    if lang:
        wikipedia.set_lang(lang)
    try:
        embed = discord.Embed(title=word,
                              description=wikipedia.summary(word),
                              color=discord.Color.blue())
    except wikipedia.exceptions.DisambiguationError as e:
        embed = discord.Embed(title='What do you mean?',
                              description='\n'.join(e.options),
                              color=discord.Color.blue())

    await ctx.send(embed=embed)


bot.run(settings['token'])
