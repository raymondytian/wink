import discord
from discord.ext import commands
import random
import time
import csv


class ModCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # purge messages
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def purge(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    # ping bot    
    @commands.command()
    async def ping(self, ctx):
        self.save(ctx, f'w!ping')
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  `{int(ping)}ms`")

    # simulates coinflip
    @commands.command()
    async def cf(self, ctx):
        if random.randint(0, 1) == 0:
            await ctx.send('Heads!')
        else:
            await ctx.send('Tails!')

    # retrieves pfp of any user
    @commands.command()
    async def pfp(self, ctx, member: discord.Member):
        embed = discord.Embed(color=0xffb6c1)
        pfp = member.avatar_url
        embed.set_author(name=f'{member}\'s profile picture:')
        embed.set_image(url=pfp)

        await ctx.send(embed=embed)

    # me
    @commands.command()
    async def dev(self, ctx):
        await ctx.send('morgan<3#7328')

    # help 
    @commands.command()
    async def help(self, ctx, arg=None):
        self.save(ctx, f'w!help {arg}')

        if arg == None:
            embed = discord.Embed(color=0xffb6c1)
            embed.set_author(name='Wink Help Center')
            embed.add_field(name='**Reddit**',
                            value='`w!help reddit`', inline=True)
            embed.add_field(name='**Other**',
                            value='`w!help commands`', inline=True)
            embed.add_field(
                name='** **', value='*morgan<3#7328*', inline=False)
            embed.set_thumbnail(url='https://lh3.googleusercontent.com/proxy/GauWOkRWww6YxYlNBBmCc9dfnCZZK1Suicq9CWOsky6sIrU_I4lo1oti7iWbK-UFiQbSI9a11CdICaaEPCBajw7UsWREXDcdCH-Jyo2IaYcGbD09W2OHx9RkhFrf3g4wKdgzxVU')

            await ctx.send(embed=embed)
        # reddit commands
        elif arg == 'reddit':
            embed = discord.Embed(title='Reddit Comands', color=0xffb6c1)
            embed.add_field(name='\u200b',
                            value='`w!image [url]\n`' +
                            'embeds image within a valid reddit submission\n\n'
                            '`w!random\n`' +
                            'embeds hottest submission in a random ' +
                            'non-nsfw subreddit\n\n' +
                            '`w!random nsfw\n`' +
                            'embeds hottest submission in a random ' +
                            'nsfw subreddit\n\n' +
                            '`w!top [x] [y]\n`' +
                            'embeds random submission from the top [y]' +
                            ' submissions in r/[x]\n\n' +
                            '`w!hot [x] [y]`\n' +
                            'embeds random submission from the hottest [y]' +
                            ' submissions in r/[x]\n\n' +
                            '`w!new [x] [y]`\n' +
                            'embeds random submission from the newest [y]' +
                            ' submissions in r/[x]\n\n', inline=True)
            embed.add_field(
                name='** **', value='*[x] defaults to r/aww if' +
                ' unspecified\n[y] defaults to 50 if unspecified*',
                inline=False)

            await ctx.send(embed=embed)
        # misc commands
        elif arg == 'commands':
            embed = discord.Embed(title='Commands', color=0xffb6c1)
            embed = discord.Embed(
                title='Miscellaneous Comands', color=0xffb6c1)
            embed.add_field(name='\u200b',
                            value='`w!ping\n`' +
                            'returns pong!\n\n' +
                            '`w!cf`\n' +
                            'simulates a coinflip\n\n' +
                            '`w!pfp @[x]`\n' +
                            'embeds pfp of member [x]\n\n', inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Invalid argument!')

    # saves incoming messages 
    def save(self, ctx, msg):
        return
        data = [str(ctx.author), str(ctx.guild.name), msg]
        data_detail = [str(ctx.message)]
        with open('messages.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        with open('messages-detail.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data_detail)


def setup(client):
    print('\n\nWink is currently running.\n\n')
    client.add_cog(ModCommands(client))
