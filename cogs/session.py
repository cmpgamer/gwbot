import asyncio
from datetime import datetime as dt
import discord
from discord.ext import commands
from gw2api import Gw2API, requestGW2AccountData
from cogs.utils.checks import embed_perms
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

        await ctx.send("Session function called")

    @session.command(pass_context=True,
                     name="start",
                     aliases=['begin'])
    async def start_session(self, ctx):
        discord_user_id = ctx.message.author.id
        await self.startGw2Session(discord_user_id)
        await ctx.send("Starting session")

    @session.command(pass_context=True,
                     name="end",
                     aliases=['stop'])
    async def end_session(self, ctx):
        discord_user_id = ctx.message.author.id
        await self.endGw2Session(discord_user_id)
        await ctx.send("Ending session")

    @session.command(pass_context=True,
                     name="wvw")
    async def wvw_session(self, ctx):
        discord_user_id = ctx.message.author.id
        result = None
        try:
            with db.create_connection(**config_data) as connection:
                with connection.cursor() as cur:
                    query = """
                        SELECT * FROM Gw2SessionInfo WHERE id = %s
                    """
                    cur.execute(
                        query,
                        (discord_user_id,)
                    )
                    result = cur.fetchone()
        except Exception as e:
            await ctx.send("Error processing !session wvw")
        else:
            #
            startAchievementInfo = {value['id']: value for value in result['startinfo']['achievements']}
            endAchievementInfo = {value['id']: value for value in result['endinfo']['achievements']}

            startDeaths = {'current': sum([character['deaths'] for character in result['startinfo']['characters']])}
            endDeaths = {'current': sum([character['deaths'] for character in result['endinfo']['characters']])}

            startTime = result['starttime']
            endTime = result['endtime']
            startWvWInfo = {
                'WvW Repairs': startAchievementInfo.get(306, {'current': 0}),
                'WvW Kills': startAchievementInfo.get(283, {'current': 0}),
                'Yak Escort': startAchievementInfo.get(285, {'current': 0}),
                'WvW Yak Kills': startAchievementInfo.get(288, {'current': 0}),
                'WvW Camps': startAchievementInfo.get(291, {'current': 0}),
                'WvW Towers': startAchievementInfo.get(297, {'current': 0}),
                'WvW Keeps': startAchievementInfo.get(300, {'current': 0}),
                'WvW Castles': startAchievementInfo.get(294, {'current': 0}),
                'Warclaw Kills': startAchievementInfo.get(4641, {'current': 0, 'repeated':0}),
                'Warclaw Gate Damage': startAchievementInfo.get(4644, {'current': 0, 'repeated':0}),
                'Deaths': startDeaths
            }
            endWvWInfo = {
                'WvW Repairs': endAchievementInfo.get(306, {'current': 0}),
                'WvW Kills': endAchievementInfo.get(283, {'current': 0}),
                'Yak Escort': endAchievementInfo.get(285, {'current': 0}),
                'WvW Yak Kills': endAchievementInfo.get(288, {'current': 0}),
                'WvW Camps': endAchievementInfo.get(291, {'current': 0}),
                'WvW Towers': endAchievementInfo.get(297, {'current': 0}),
                'WvW Keeps': endAchievementInfo.get(300, {'current': 0}),
                'WvW Castles': endAchievementInfo.get(294, {'current': 0}),
                'Warclaw Kills': endAchievementInfo.get(4641, {'current': 0, 'repeated':0}),
                'Warclaw Gate Damage': endAchievementInfo.get(4644, {'current': 0, 'repeated':0}),
                'Deaths': endDeaths
            }
            # print(startWvWInfo)
            # Normalize Warclaw Kills
            if 'repeated' in startWvWInfo['Warclaw Kills']:
                startWvWInfo['Warclaw Kills']['current'] += startWvWInfo['Warclaw Kills']['repeated'] * 5
                endWvWInfo['Warclaw Kills']['current'] += endWvWInfo['Warclaw Kills']['repeated'] * 5

            # Normalize Warclaw Gate Damage
            if 'repeated' in startWvWInfo['Warclaw Gate Damage']:
                startWvWInfo['Warclaw Gate Damage']['current'] += startWvWInfo['Warclaw Gate Damage']['repeated'] * 100000
                endWvWInfo['Warclaw Gate Damage']['current'] += endWvWInfo['Warclaw Gate Damage']['repeated'] * 100000

            # Get the difference between each current value in the WvWInfo Dicts
            wvwDiff = {key: endWvWInfo[key]['current'] - startWvWInfo[key]['current'] for key in startWvWInfo.keys()}
            print(wvwDiff['Deaths'])
            # Calculate time difference
            timeElapsed = endTime - startTime
            hours, remainder = divmod(timeElapsed.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            playTimeStr = "{}h {}m {}s".format(hours, minutes, seconds)

            embed_time_format = "%X UTC"

            user = ctx.message.author
            if embed_perms(ctx.message):

                desc = """
                    You started playing at **{}** and stopped at **{}** for a total playtime of **{}**\n
                    \n
                    `Note: Deaths are tracked globally`
                """.format(startTime.strftime(embed_time_format), endTime.strftime(embed_time_format), playTimeStr)
                # Default to the numerator if denominator is 0 for Kill Death Ratio
                wvw_kdr = wvwDiff['WvW Kills'] / wvwDiff['Deaths'] if wvwDiff['Deaths'] else wvwDiff['WvW Kills']
                em = discord.Embed(title="WvW Session Stats", description=desc, timestamp=ctx.message.created_at, color=0xFF0000)
                # Playtime information
                # KDR
                em.add_field(name='WvW Kills :crossed_swords:', value=wvwDiff['WvW Kills'], inline=True)
                em.add_field(name='Deaths :skull:', value=wvwDiff['Deaths'], inline=True)
                em.add_field(name='KDR', value=wvw_kdr, inline=True)
                # Zero Width space unicode character
                # em.add_field(name='\u200b', value='\u200b', inline=False)
                # WvW Information
                em.add_field(name='Camps Flipped :circus_tent:', value=wvwDiff['WvW Camps'], inline=True)
                em.add_field(name='Towers Seized :synagogue:', value=wvwDiff['WvW Towers'], inline=True)
                em.add_field(name='Keeps Captured :european_castle:', value=wvwDiff['WvW Keeps'], inline=True)
                em.add_field(name='Castles Liberated :japanese_castle:', value=wvwDiff['WvW Castles'], inline=True)
                em.add_field(name='Yaks Slapped :meat_on_bone:', value=wvwDiff['WvW Yak Kills'], inline=True)
                em.add_field(name='Yaks Escorted :ram:', value=wvwDiff['Yak Escort'], inline=True)
                em.add_field(name='Supply Spent Repairing :tools:', value=wvwDiff['WvW Repairs'], inline=True)
                em.add_field(name='Warclaw Maul Kills :lion:', value=wvwDiff['Warclaw Kills'], inline=True)
                em.add_field(name='Warclaw Gate Damage :shinto_shrine:', value=wvwDiff['Warclaw Gate Damage'], inline=True)
                em.set_author(name=user.display_name, icon_url=user.avatar_url)
                await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """ Listener for when members update their Activity

        :param before:
        :param after:
        :return:
        """
        if after and after.activity is not None:
            if after.activity.name == "Guild Wars 2":
                print(after.id)
                await self.startGw2Session(after.id)
                print("Started GW2 Session {} {}".format(after, dt.utcnow()))

        elif before and before.activity is not None:
            if before.activity.name == "Guild Wars 2":
                await self.endGw2Session(before.id)
                print("Ending GW2 Session {} {}".format(before, dt.utcnow()))

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
        results = Json(results)
        # Insert all JSON data into database
        try:
            with db.create_connection(**config_data) as connection:
                with connection.cursor() as cur:
                    query = """
                        INSERT INTO Gw2SessionInfo (id, StartInfo, StartTime) VALUES (%s, %s, %s)
                        ON CONFLICT (id) DO UPDATE SET
                        (StartInfo, StartTime) = (EXCLUDED.StartInfo, EXCLUDED.StartTime)
                    """
                    cur.execute(
                        query,
                        (discord_user_id, results, dt.utcnow(),)
                    )
                    connection.commit()
        except Exception as e:
            print(e)

    async def endGw2Session(self, discord_user_id: int):

        results = await self.getGw2AccountDataFromUserId(discord_user_id)
        results = Json(results)
        # Insert all JSON data into database
        try:
            with db.create_connection(**config_data) as connection:
                with connection.cursor() as cur:
                    query = """
                                INSERT INTO Gw2SessionInfo (id, EndInfo, EndTime) VALUES (%s, %s, %s)
                                ON CONFLICT (id) DO UPDATE SET
                                (EndInfo, EndTime) = (EXCLUDED.EndInfo, EXCLUDED.EndTime)
                            """
                    cur.execute(
                        query,
                        (discord_user_id, results, dt.utcnow())
                    )
                    connection.commit()
        except Exception as e:
            print(e)

    async def insertOrUpdateAccountInfo(self, discord_user_id: int):
        results = await self.getGw2AccountDataFromUserId(discord_user_id)
        results = {key: Json(value) for (key, value) in results.items()}
        # Insert all JSON data into database
        try:
            with db.create_connection(**config_data) as connection:
                with connection.cursor() as cur:
                    query = """
                        INSERT INTO Gw2AccountInfo VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                         ON CONFLICT (id) DO UPDATE SET 
                         (account, achievements, skins, titles, minis, outfits, dyes, finishers, wallet, materials, 
                            bank, inventory, pvp, characters)
                         = (EXCLUDED.account, EXCLUDED.achievements, EXCLUDED.skins, EXCLUDED.titles, EXCLUDED.minis, 
                            EXCLUDED.outfits, EXCLUDED.dyes, EXCLUDED.finishers, EXCLUDED.wallet, EXCLUDED.materials, 
                            EXCLUDED.bank, EXCLUDED.inventory, EXCLUDED.pvp, EXCLUDED.characters)
                    """
                    cur.execute(
                        query,
                        (discord_user_id, results['account'], results['achievements'], results['skins'],
                         results['titles'], results['minis'], results['outfits'], results['dyes'], results['finishers'],
                         results['wallet'], results['materials'], results['bank'], results['inventory'], results['pvp'],
                         results['characters'])
                    )
                    connection.commit()
        except Exception as e:
            print(e)

    async def getCurrentGw2AccountInfo(self, discord_user_id: int):
        results = None
        try:
            with db.create_connection(**config_data) as connection:
                with connection.cursor() as cur:
                    query = """
                        SELECT * FROM Gw2AccountInfo WHERE id = %s
                    """
                    cur.execute(
                        query,
                        (discord_user_id,)
                    )
                    results = cur.fetchone()

        except Exception as e:
            print(e)
        return results

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
    result = None
    try:
        with db.create_connection(**config_data) as connection:
            with connection.cursor() as cur:
                print("In getUserAPIKey(). DiscordId: ", discord_id)
                cur.execute("SELECT api_key FROM Gw2ApiKeys WHERE id = %s", (discord_id,))
                result = cur.fetchone()['api_key']
                print(result)
    except Exception as e:
        print(e)
    return result
