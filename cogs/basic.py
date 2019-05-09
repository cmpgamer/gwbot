import discord
from discord.ext import commands
from datetime import datetime

from cogs.session import getUserAPIKey
from gw2api import Gw2API

all_perms = ['tradingpost', 'characters', 'pvp', 'progression', 'wallet', 'guilds', 'builds', 'account', 'inventories', 'unlocks']

class Basic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ls3trinkets",
        description="A command to upload the Living Story 3 trinkets",
        aliases=["trinkets"]
    )
    async def trinkets_command(self, ctx):
        await ctx.send(file=discord.File('./images/LS3Trinkets.jpg'))
    
    @commands.command(
        name="emojis",
        description="A command to print out all emojis"
    )
    async def emojis_command(self, ctx):
        emojis = ctx.guild.emojis
        message = ctx.message
        for emoji in emojis:
            await message.add_reaction(emoji)

    @commands.command(
        name="doc",
        description="A random command",
        aliases=['Doc', 'Document', 'document', 'guilddoc', 'GuildDoc', 'Guilddoc', 'gd']
    )
    async def doc(self, ctx):
        embed=discord.Embed(
            title="google",
            url="https://google.com/",
            description="Google woo",
            color=0xff8040,
            timestamp=ctx.message.created_at
        )
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """
        A decorated message that registers the 'on_message' Event to the bot
        """
        time = datetime.now()
        if message.author.bot:
            return
        print("[{0.created_at}] {0.display_name}({0.name}) {0.id} - {1}".format(message.author, message.content))

    async def cog_command_error(self, ctx, error):
        time = datetime.now()
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    @commands.command(
       name="permissions",
       description="Outputs a list of all permissions the user has.",
       aliases=['perms']
    )
    async def getPermissions(self, ctx):
        discord_user_id = ctx.message.author.id
        api_key = await getUserAPIKey(discord_user_id)
        if api_key:
            # Create an instance of the Gw2API object
            gw2UserAPIInstance = Gw2API(api_key)

            em = discord.Embed()
            for perm in all_perms:

                if perm in gw2UserAPIInstance.permissions:
                    val = ":white_check_mark:"
                else:
                    val = ":x:"
                perm = perm.capitalize()
                em.add_field(name=perm, value=val, inline=True)


            await ctx.send(embed=em)
        else:
            await ctx.send("You do not have an API Key stored ")

def setup(bot):
    """
    Adds the Basic commands to the bot
    """
    print("I GET HERE")
    bot.add_cog(Basic(bot))