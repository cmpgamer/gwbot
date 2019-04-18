from discord.ext import commands
from database import models as db


class Character:

    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(pass_context=True)
    async def characters(self, ctx, character_name=''):
        if ctx.invoked_subcommand is None:
            if character_name:
                #print all info on cahracter
                pass
            else:
                # print all cahracters on account
                pass
            return
    
    @character.command(pass_context=True)
    async def add(self, ctx, key: str):
        discord_user = ctx.message.author.name
        if not check_key_exists(discord_user):
            session = db.Session()
            new_key = db.Keys.__table__.insert().values(
                discord_id=discord_user, gw2_api_key=key
            )
            session.execute(new_key)
            try:
                session.commit()
            except Exception as e:
                pass
        else:
            pass
            # update key?
    
    def check_key_exists(self, user):
        """
        
        """
        session = db.Session()
        results = session.query(db.Keys).filter_by(discord_id=user).one_or_none()
        if results:
            return True
        return False    
        
        
def setup(bot):
    bot.add_cog(Api(bot))  