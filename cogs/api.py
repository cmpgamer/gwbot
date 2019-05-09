from discord.ext import commands
from database import database as db
import json
import psycopg2.extensions

with open('./database/db_settings.json') as json_file:
    config_data = json.load(json_file)['PostgresDatabase']

class Api(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(pass_context=True)
    async def api(self, ctx):
        if ctx.invoked_subcommand is None:
            return
    
    @api.command(pass_context=True)
    async def add(self, ctx, key: str):
        connection = db.create_connection(**config_data)
        discord_user_id = ctx.message.author.id
        if not self.check_key_exists(connection, discord_user_id):
            try:
                cur = connection.cursor()
                cur.execute("INSERT INTO Gw2ApiKeys VALUES (%s, %s)", (discord_user_id, key))
                await ctx.send("Adding new key to be tracked.")
                connection.commit()
            except Exception as e:
                print(e)
        else:
            try:
                cur = connection.cursor()
                cur.execute("UPDATE Gw2ApiKeys SET api_key = %s WHERE id = %s", (key, discord_user_id))
                await ctx.send("Key already stored. Updating old API key with new key.")
                connection.commit()
            except Exception as e:
                await ctx.send("There was an error storing your API key. Please try again later.")
                print(e)
        connection.close()
    
    def check_key_exists(self, connection : psycopg2._psycopg.connection, user: str) -> bool:
        result = []
        try:
            cur = connection.cursor()
            cur.execute("SELECT * FROM Gw2ApiKeys WHERE id = %s", (user,))
            result = cur.fetchone()
        except Exception as e:
            print(e)
        if result:
            return True
        return False    
        
        
def setup(bot):
    bot.add_cog(Api(bot))  