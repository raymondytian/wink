import discord
from discord.ext import commands
import os
from itertools import cycle
import json

client = commands.Bot(command_prefix='w!')
client.remove_command('help')

# reloads commands when changes are made in cogs
@client.command()
async def reload(ctx, after=""):
    if after != "":
        return
    if not str(ctx.author.id) == '524758183886192653':
        await ctx.send('Access denied.')
        return
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
            client.load_extension(f'cogs.{filename[:-3]}')
    await ctx.send('Cogs reloaded.')


# loads cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

TOKEN = os.environ.get('TOKEN')
client.run(TOKEN)
