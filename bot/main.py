import discord
from discord.ext import commands
import os
from itertools import cycle
import json
import csv

client = commands.Bot(command_prefix='w!')
client.remove_command('help')


# saves incoming messages 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('w!'):
        data = [str(message.author), str(message.content), str(message.created_at), str(message.author.id)]
        with open('messages.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)

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

# retrieves token to run bot
with open('./config.json') as f:
    data = json.load(f)

TOKEN = data['Token']
client.run(TOKEN)
