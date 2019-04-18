
import requests
import aiohttp
from utils.endpoints import *

class Gw2API(object):
    baseURL = "https://api.guildwars2.com{}"
    
    def __init__(self, token):
        self.token = token
        self.header = {
            'X-Schema-Version': '2019-02-21T00:00:00Z',
            'Authorization': "Bearer {0}".format(self.token)
        }
        tokenInfo = self.getTokenInfo()
        self.permissions = tokenInfo['permissions']
        self.session = aiohttp.ClientSession()

    def __del__(self):
        self.session._connector.close()

    def getTokenInfo(self):
        response = requests.get(self.baseURL.format(TOKENINFO), headers=self.header)
        return response.json()

    async def getAccount(self):
        response = None
        if "progression" in self.permissions:
            async with self.session.get(self.baseURL.format(ACCOUNT), headers=self.header) as resp:
                response = await resp.json()
        return response

    async def getAccountAchievements(self):
        response = None
        if "progression" in self.permissions:
            async with self.session.get(self.baseURL.format(ACCOUNT_ACHIEVEMENTS), headers=self.header) as resp:
                response = await resp.json()
        return response

    async def getAccountBank(self):
        response = None
        if 'inventories' in self.permissions:
            async with self.session.get(self.baseURL.format(ACCOUNT_BANK), headers=self.header) as resp:
                response = await resp.json()
        return response

    async def getAccountDungeons(self):
        async with self.session.get(self.baseURL.format(ACCOUNT_DUNGEONS), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getAccountDyes(self):
        response = None
        if 'unlocks' in self.permissions:
            async with self.session.get(self.baseURL.format(ACCOUNT_DYES), headers=self.header) as resp:
                response = await resp.json()
        return response

    async def getAccountFinishers(self):
        response = None
        if 'unlocks' in self.permissions:
            async with self.session.get(self.baseURL.format(ACCOUNT_FINISHERS), headers=self.header) as resp:
                response = await resp.json()
        return response

    async def getAccountGliders(self):
        async with self.session.get(self.baseURL.format(ACCOUNT_GLIDERS), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getAccountHomeCats(self):
        async with self.session.get(self.baseURL.format(ACCOUNT_HOME_CATS), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getAccountHomeNodes(self):
        async with self.session.get(self.baseURL.format(ACCOUNT_HOME_NODES), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getAccountInventory(self):
        async with self.session.get(self.baseURL.format(ACCOUNT_INVENTORY), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getAccountMailCarriers(self):
        async with self.session.get(self.baseURL.format(ACCOUNT_MAILCARRIERS), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getAccountMasteries(self):
        async with self.session.get(self.baseURL.format(ACCOUNT_MASTERIES), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getAccountMaterials(self):
        response = None
        if 'unlocks' in self.permissions:
            async with self.session.get(self.baseURL.format(ACCOUNT_MATERIALS), headers=self.header) as resp:
                response = await resp.json()
        return response

    async def getAccountMinis(self):
        response = None
        if 'unlocks' in self.permissions:
            async with self.session.get(self.baseURL.format(ACCOUNT_MINIS), headers=self.header) as resp:
                response = await resp.json()
        return response

    async def getAccountMountSkins(self):
        async with self.session.get(self.baseURL.format(ACCOUNT_MOUNTS_SKINS), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getAccountMountsType(self):
        async with self.session.get(self.baseURL.format(ACCOUNT_MOUNTS_TYPE), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getAccountOutfits(self):
        response = None
        if 'unlocks' in self.permissions:
            async with self.session.get(self.baseURL.format(ACCOUNT_OUTFITS), headers=self.header) as resp:
                response = await resp.json()
        return response

    async def getAccountPvPHeroes(self):
        async with self.session.get(self.baseURL.format(ACCOUNT_PVP_HEROES), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getAccountRaids(self):
        async with self.session.get(self.baseURL.format(ACCOUNT_RAIDS), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getAccountRecipes(self):
        async with self.session.get(self.baseURL.format(ACCOUNT_RECIPES), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getAccountSkins(self):
        response = None
        if 'unlocks' in self.permissions:
            async with self.session.get(self.baseURL.format(ACCOUNT_SKINS), headers=self.header) as resp:
                response = await resp.json()
        return response

    async def getAccountTitles(self):
        response = None
        if 'unlocks' in self.permissions:
            async with self.session.get(self.baseURL.format(ACCOUNT_TITLES), headers=self.header) as resp:
                response = await resp.json()
        return response

    async def getAccountWallet(self):
        response = None
        if 'wallet' in self.permissions:
            async with self.session.get(self.baseURL.format(ACCOUNT_WALLET), headers=self.header) as resp:
                response = await resp.json()
        return response

    async def getCharacters(self):
        response = None
        if 'characters' in self.permissions:
            async with self.session.get(self.baseURL.format(CHARACTERS), headers=self.header) as resp:
                response = await resp.json()
        return response

    async def getCharactersEquipment(self):
        # TODO
        async with self.session.get(self.baseURL.format(CHARACTER_EQUIPMENT), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getCharactersInventory(self):
        # TODO
        async with self.session.get(self.baseURL.format(CHARACTER_INVENTORY), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getCommerceTransactions(self):
        async with self.session.get(self.baseURL.format(COMMERCE_TRANSACTIONS), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getPvPStats(self):
        response = None
        if 'pvp' in self.permissions:
            async with self.session.get(self.baseURL.format(PVP_STATS), headers=self.header) as resp:
                response = await resp.json()
        return response

    async def getPvPGames(self):
        async with self.session.get(self.baseURL.format(PVP_GAMES), headers=self.header) as resp:
            response = await resp.json()
        return response

    async def getPvPStandings(self):
        async with self.session.get(self.baseURL.format(PVP_STANDINGS), headers=self.header) as resp:
            response = await resp.json()
        return response

async def requestGW2AccountData(userGw2API: Gw2API) -> dict:
    """
    Gathers all of the Guild Wars 2 account data that relies on permissions set when creating the API Key.
    :param userGw2API: An instance of the Gw2API class to tailor each API call by Discord User's API Key.
    :return: dict: A dictionary of each of the account information fields.
    """
    queries = {
        'account': await userGw2API.getAccount(),
        'achievements': await userGw2API.getAccountAchievements(),
        'skins': await userGw2API.getAccountSkins(),
        'titles': await userGw2API.getAccountTitles(),
        'minis': await userGw2API.getAccountMinis(),
        'outfits': await userGw2API.getAccountOutfits(),
        'dyes': await userGw2API.getAccountDyes(),
        'finishers': await userGw2API.getAccountFinishers(),
        'wallet': await userGw2API.getAccountWallet(),
        'materials': await userGw2API.getAccountMaterials(),
        'bank': await userGw2API.getAccountBank(),
        'inventory': await userGw2API.getAccountInventory(),
        'pvp': await userGw2API.getPvPStats(),
        'characters': await userGw2API.getCharacters()
    }
    return queries