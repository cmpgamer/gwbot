import asyncio
import discord
import datetime
import time
import pickle
import json
import discord
from discord.ext.commands import Bot
import pattern
import logging
from cogs import basic


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

config_data = None
with open('./settings/config.json') as json_file:
    config_data = json.load(json_file)

cogs = ['cogs.basic', 'cogs.wvw', 'cogs.user', 'cogs.session', 'cogs.api']

bot = Bot(command_prefix=config_data['cmd_prefix'], description=config_data['description'])

"""
When having issues with the discord context, you can view the context object's contents, view the object here
discord.ext.commands.context.Context.<content>
"""


@bot.event
async def on_ready():
    print('Logged in as: {0.name}({1.id})'.format(bot.user, bot.user))
    print('Invite: https://discordapp.com/oauth2/authorize?client_id={0.id}&scope=bot'.format(bot.user))
    class_list = ["mesmer", "necromancer", "elementalist", "thief", "engineer", "ranger", "warrior", "guardian", "revenant"]
    emoji_list = []
    # server = bot.get_server("306910538255040522")
    
    # for emoji in server.emojis:
    #     for profession in class_list:
    #         if profession not in emoji_list and profession == emoji.name:
    #             emoji_list.append(emoji)
    # bot.profession_emojis = emoji_list
    # print(database.engine)


def main():
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(cog, exc))
    
    bot.run(config_data['token'], bot=True, reconnect=True)

if __name__ == "__main__":
    main()
