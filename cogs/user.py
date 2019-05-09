import discord
from discord.ext import commands
from cogs.utils.checks import embed_perms, cmd_prefix_len
from datetime import datetime

'''Module for the info command.'''



class Userinfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    @commands.group(invoke_without_command=True, pass_context=True, aliases=['ui', 'userinfo'])
    async def user(self, ctx, name=""):
        """Get user info."""
        if ctx.invoked_subcommand is None:
            pre = cmd_prefix_len()
            if name:
                try:
                    user = ctx.message.mentions[0]
                except IndexError:
                    user = ctx.guild.get_member_named(name)
                if not user:
                    user = ctx.guild.get_member(name)
                if not user:
                    await ctx.send('Could not find user.')
                    return
            else:
                user = ctx.message.author
        
            # Thanks to IgneelDxD for help on this
            if user.avatar_url[54:].startswith('a_'):
                avi = 'https://images.discordapp.net/avatars/' + user.avatar_url[35:-10]
            else:
                avi = user.avatar_url
            if isinstance(user, discord.Member):
                role = user.top_role.name
                if role == "@everyone":
                    role = "N/A"
                voice_state = user.voice
            if embed_perms(ctx.message):
                
                time = ctx.message.created_at.strftime('%m/%d/%Y %H:%M:%S')
                em = discord.Embed(timestamp=ctx.message.created_at, color=0x708DD0)
                em.add_field(name='User ID', value=user.id, inline=True)
                if isinstance(user, discord.Member):
                    em.add_field(name='Nickname', value=user.nick, inline=True)
                    em.add_field(name='Status', value=user.status, inline=True)
                    em.add_field(name='In Voice', value=voice_state, inline=True)
                    em.add_field(name='Game', value=user.activity, inline=True)
                    em.add_field(name='Highest Role', value=role, inline=True)
                em.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
                if isinstance(user, discord.Member):
                    em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
                em.set_thumbnail(url=avi)
                em.set_author(name=user, icon_url=user.avatar_url)
                await ctx.send(embed=em)
            else:
                if isinstance(user, discord.Member):
                    msg = '**User Info:** ```User ID: %s\nNick: %s\nStatus: %s\nIn Voice: %s\nGame: %s\nHighest Role: %s\nAccount Created: %s\nJoin Date: %s\nAvatar url:%s```' % (user.id, user.nick, user.status, voice_state, user.game, role, user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), avi)
                else:
                    msg = '**User Info:** ```User ID: %s\nAccount Created: %s\nAvatar url:%s```' % (user.id, user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), avi)
                await ctx.send(msg)
            
    @user.command(pass_context=True)
    async def info(self, ctx, name=""):
        """Get a detailed embed of user info. Ex: ~user info [name|nickname|user-id]"""
        pass

    @user.command(pass_context=True)
    async def avi(self, ctx, name: str = None):
        """View bigger version of user's avatar. Ex: ~userinfo avi @user"""
        if name:
            try:
                user = ctx.message.mentions[0]
            except IndexError:
                user = ctx.guild.get_member_named(name)
            if not user:
                user = ctx.guild.get_member(name)
            if not user:
                await ctx.send('Could not find user {}'.format(name))
                return
        else:
            user = ctx.message.author

        print(user)
        # Thanks to IgneelDxD for help on this
        if user.avatar_url[54:].startswith('a_'):
            avi = 'https://images.discordapp.net/avatars/' + user.avatar_url[35:-10]
        else:
            avi = user.avatar_url
        if embed_perms(ctx.message):
            em = discord.Embed(color=0x708DD0)
            em.set_image(url=avi)
            await ctx.send(embed=em)
        else:
            await ctx.send(avi)


def setup(bot):
    bot.add_cog(Userinfo(bot))