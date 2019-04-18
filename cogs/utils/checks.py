import json
import time
import discord
import os

def load_config():
    with open('settings/config.json', 'r') as f:
        return json.load(f)

def cmd_prefix_len():
    config = load_config()
    return len(config['cmd_prefix'])


def embed_perms(message):
    try:
        check = message.author.permissions_in(message.channel).embed_links
    except:
        check = True
    return check