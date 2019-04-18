import asyncio
from datetime import datetime

from discord.ext import commands
from gw2api import Gw2API, requestGW2AccountData
from database import database as db

from utils.api import *

with open('./database/db_settings.json') as json_file:
    config_data = json.load(json_file)['PostgresDatabase']


class Session(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, pass_context=True)
    async def session(self, ctx):
        """
        TODO This is just a stub for now. Eventually it will compare the difference between each account information
        TODO from "last login time" and "most up to date"
        :param ctx: Discord Context object created from each command.
        :return: Sends a message to the channel where the user instantiated the command.
        """
        discord_user_id = ctx.message.author.id
        results = self.gatherGw2AccountData(discord_user_id)
        # Convert all nested dicts to psycopg.Json object to store

        # Insert all JSON data into database
        try:
            with db.create_connection(**config_data) as connection:
                with connection.cursor() as cur:
                    cur.execute(
                        "INSERT INTO Gw2AccountInfo VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (discord_user_id, results['account'], results['achievements'], results['skins'], results['titles'],
                         results['minis'], results['outfits'], results['dyes'], results['finishers'], results['wallet'],
                         results['materials'], results['bank'], results['inventory'], results['pvp'], results['characters'])
                    )
                    connection.commit()
        except Exception as e:
            print(e)

        await ctx.send("Done grabbing session data")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            print("Before {} \t After {}".format(before.activity.name,after.activity.name))
        except Exception as e:
            print(e)

        if after.activity.name is not None:
            if after.activity.name == "Guild Wars 2":
                await self.startGw2Session(after.id)
                print("started gw2 session")


        elif before.activity.name is not None:
            if before.activity.name == "Guild Wars 2":
                await self.endGw2Session(before.id)
                print("ended gw2 session")


    async def getGw2AccountDataFromUserId(self, discord_user_id):
        # Get the Discord User ID from the message context
        # discord_user_id = ctx.message.author.id
        # Get the API key from the database
        api_key = await getUserAPIKey(discord_user_id)
        # Create an instance of the Gw2API object
        gw2UserAPIInstance = Gw2API(api_key)
        # Gather Account data from GW2 API servers
        results = await requestGW2AccountData(gw2UserAPIInstance)
        return results


    async def startGw2Session(self, discord_user_id: int):
        results = await self.getGw2AccountDataFromUserId(discord_user_id)
        results = {key: Json(value) for (key, value) in results.items()}
        # Insert all JSON data into database
        try:
            with db.create_connection(**config_data) as connection:
                with connection.cursor() as cur:
                    cur.execute(
                        "INSERT INTO Gw2AccountInfo VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (discord_user_id, results['account'], results['achievements'], results['skins'],
                         results['titles'],
                         results['minis'], results['outfits'], results['dyes'], results['finishers'], results['wallet'],
                         results['materials'], results['bank'], results['inventory'], results['pvp'],
                         results['characters'])
                    )
                    connection.commit()
        except Exception as e:
            print(e)

    async def endGw2Session(self, discord_user_id: int):
        results = self.getGw2AccountDataFromUserId(discord_user_id)
        results = {key: Json(value) for (key, value) in results.items()}
        # Insert all JSON data into database
        try:
            with db.create_connection(**config_data) as connection:
                with connection.cursor() as cur:
                    cur.execute(
                        "INSERT INTO Gw2AccountInfo VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (discord_user_id, results['account'], results['achievements'], results['skins'],
                         results['titles'],
                         results['minis'], results['outfits'], results['dyes'], results['finishers'], results['wallet'],
                         results['materials'], results['bank'], results['inventory'], results['pvp'],
                         results['characters'])
                    )
                    connection.commit()
        except Exception as e:
            print(e)


def setup(bot):
    """
    Adds the Session commands to the bot
    """
    bot.add_cog(Session(bot))

async def getUserAPIKey(discord_id: int) -> str:
    """
    Get the Discord User's API key from the database and return it.
    :param discord_id: The Discord User Account ID from message context object.
    :return: str: The Discord User's API Key.
    """
    result = ""
    try:
        with db.create_connection(**config_data) as connection:
            with connection.cursor() as cur:
                cur.execute("SELECT api_key FROM Gw2ApiKeys WHERE id = %s", (discord_id,))
                result = cur.fetchone()
    except Exception as e:
        print(e)
    return result