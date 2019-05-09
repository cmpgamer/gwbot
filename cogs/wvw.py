import discord
from discord.ext import commands
from datetime import datetime

class WvW(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="d",
        description="A command to upload the Living Story 3 trinkets",
    )
    async def trinkets_command(self, ctx):
        await ctx.send(file=discord.File('./images/LS3Trinkets.jpg'))
    
    @commands.Cog.listener()
    async def wvw_command_error(self, ctx, error):
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
    bot.add_cog(WvW(bot))