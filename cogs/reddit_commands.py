import discord
from discord.ext import commands
import praw
import random
from prawcore import NotFound
import csv


class RedditCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(client_id='InK7xDDqjhhJ1A',
                                  client_secret='HSi9Zh9dhPIu7oS-EAOqBMpB_H4',
                                  user_agent='Wink',
                                  username='wink_bot',
                                  password='TYQ123rt$')

    # see if subreddit exists
    def sub_exists(self, sub='aww'):
        try:
            self.reddit.subreddits.search_by_name(sub, exact=True)
        except NotFound:
            return False
        return True

    # see if subreddit has image submissions
    def has_submissions(self, subreddit=None):
        if subreddit == None:
            return False
        for submission in subreddit.hot(limit=1):
            if submission.url.endswith('jpg') or \
                    submission.url.endswith('png'):
                return True
        return False

    # see if submission has image
    def has_image(self, submission=None):
        if submission == None:
            return False
        if submission.url.endswith('jpg') or \
                submission.url.endswith('png'):
            return True
        return False

    # sends image embed
    @commands.command()
    async def send_embed(self, ctx, submission=None):
        if submission == None:
            return
        embed = discord.Embed(
            title=submission.title, description='Already seen this submission?' +
            ' Try \'w!help reddit\'', color=0xffb6c1)
        embed.set_image(url=submission.url)
        await ctx.send(embed=embed)

    # sends image in reddit submission link
    @commands.command()
    async def image(self, ctx, link=""):
        self.save(ctx, f'w!random {link}')

        if link == "":
            await ctx.send("Please enter a reddit link along with w!image")
            return
        try:
            submission = self.reddit.submission(url=link)
        except:
            await ctx.send("Please enter a valid link")
            return
        if self.has_image(submission):
            await self.send_embed(ctx, submission)

    # sends random image in a random subreddit
    @commands.command()
    async def random(self, ctx, nsfw=""):
        self.save(ctx, f'w!random {nsfw}')

        has_submissions = False

        while has_submissions == False:
            if nsfw == "nsfw":
                subreddit = self.reddit.random_subreddit(True)
            else:
                subreddit = self.reddit.random_subreddit()

            has_submissions = self.has_submissions(subreddit)

        await self.hot(ctx, str(subreddit), 1)

    # sends a top x image sorted by hot from subreddit
    @commands.command()
    async def hot(self, ctx, sub='aww', lim=50):
        self.save(ctx, f'w!hot {sub} {lim}')

        if self.sub_exists(sub) == False:
            await ctx.send('Invalid subreddit!')
            return

        subreddit = self.reddit.subreddit(sub)
        if not ctx.channel.is_nsfw() and subreddit.over18:
            await ctx.send('This subreddit can only be called in channels' +
                           ' marked NSFW!')
            return

        submissions = []

        try:
            for submission in subreddit.hot(limit=1):
                submission.title
        except Exception:
            await ctx.send('This subreddit has been removed!')
            return

        for submission in subreddit.hot(limit=lim):
            if self.has_image(submission):
                submissions.append(submission)

        if len(submissions) == 0:
            await ctx.send('This subreddit returned 0 images! Try again!')
            return

        chosen = random.choice(submissions)

        if not ctx.channel.is_nsfw() and chosen.over_18:
            await ctx.send('This submission can only be seen in channels' +
                           ' marked NSFW!')
            return

        await self.send_embed(ctx, chosen)

    # sends a top x image sorted by top from subreddit
    @commands.command()
    async def top(self, ctx, sub='aww', lim=50):
        self.save(ctx, f'w!top {sub} {lim}')

        if self.sub_exists(sub) == False:
            await ctx.send('Invalid subreddit!')
            return

        subreddit = self.reddit.subreddit(sub)

        if not ctx.channel.is_nsfw() and subreddit.over18:
            await ctx.send('This subreddit can only be called in channels ' +
                           'marked NSFW!')
            return

        submissions = []

        try:
            for submission in subreddit.top(limit=1):
                submission.title
        except Exception:
            await ctx.send('This subreddit has been removed!')
            return

        for submission in subreddit.top(limit=lim):
            if self.has_image(submission):
                submissions.append(submission)

        if len(submissions) == 0:
            await ctx.send('This subreddit returned 0 images! Try again!')
            return

        chosen = random.choice(submissions)

        if not ctx.channel.is_nsfw() and chosen.over_18:
            await ctx.send('This submission can only be seen in channels' +
                           ' marked NSFW!')
            return

        await self.send_embed(ctx, chosen)

    # sends a new x image sorted by new from subreddit
    @commands.command()
    async def new(self, ctx, sub='aww', lim=50):
        self.save(ctx, f'w!new {sub} {lim}')

        if self.sub_exists(sub) == False:
            await ctx.send('Invalid subreddit!')
            return

        subreddit = self.reddit.subreddit(sub)

        if not ctx.channel.is_nsfw() and subreddit.over18:
            await ctx.send('This subreddit can only be called in channels' +
                           ' marked NSFW!')
            return

        submissions = []

        try:
            for submission in subreddit.new(limit=1):
                submission.title
        except Exception:
            await ctx.send('This subreddit has been removed!')
            return

        for submission in subreddit.new(limit=lim):
            if self.has_image(submission):
                submissions.append(submission)

        if len(submissions) == 0:
            await ctx.send('This subreddit returned 0 images! Try again!')
            return

        chosen = random.choice(submissions)

        if not ctx.channel.is_nsfw() and chosen.over_18:
            await ctx.send('This submission can only be seen in channels ' +
                           'marked NSFW!')
            return

        await self.send_embed(ctx, chosen)

    # saves incoming messages 
    def save(self, ctx, msg):
        data = [str(ctx.author), str(ctx.guild.name), msg]
        data_detail = [str(ctx.message)]
        with open('messages.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        with open('messages-detail.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data_detail)


def setup(client):
    client.add_cog(RedditCommands(client))
