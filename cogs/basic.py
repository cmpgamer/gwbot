import discord
from discord.ext import commands
from datetime import datetime

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

    # @commands.Cog.listener()
    # async def on_member_update(self, before, after):
    #     print('we got here')
    #     if before is not None and after is not None:
    #         if after.activity.name == "Guild Wars 2":
    #             # Grab initial data from GW2 API
    #             pass
    #
    #         if before.activity.name == "Guild Wars 2":
    #             pass

def setup(bot):
    """
    Adds the Basic commands to the bot
    """
    bot.add_cog(Basic(bot))