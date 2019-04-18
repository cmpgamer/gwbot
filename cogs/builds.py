import asyncio
import discord

import datetime
from discord.ext import commands
import pattern
from database import models as db
from sqlalchemy.exc import InvalidRequestError

class_thumbnails = {
    "Mesmer" : "https://wiki.guildwars2.com/images/3/3a/Mesmer_icon.png",
    "Necromancer" : "https://wiki.guildwars2.com/images/6/62/Necromancer_icon.png",
    "Elementalist" : "https://wiki.guildwars2.com/images/a/a2/Elementalist_icon.png",
    "Thief" : "https://wiki.guildwars2.com/images/d/d8/Thief_icon.png",
    "Engineer" : "https://wiki.guildwars2.com/images/4/41/Engineer_icon.png",
    "Ranger" : "https://wiki.guildwars2.com/images/9/9c/Ranger_icon.png",
    "Warrior" : "https://wiki.guildwars2.com/images/c/c8/Warrior_icon.png",
    "Guardian" : "https://wiki.guildwars2.com/images/c/cc/Guardian_icon.png",
    "Revenant" : "https://wiki.guildwars2.com/images/8/89/Revenant_icon.png",
}

class_colors = {
    "Mesmer" : 0xd42aff,
    "Necromancer" : 0x1dbb72,
    "Elementalist" : 0xd46161,
    "Thief" : 0x89676d,
    "Engineer" : 0xcf7f4c,
    "Ranger" : 0x93c349,
    "Warrior" : 0xdcb45d,
    "Guardian" : 0x60bcd3,
    "Revenant" : 0xa60000,
}



class Builds:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, pass_context=True)
    async def builds(self, ctx, profession=""):
        """
        Print stored GW2 WvW builds info. Ex: ~builds <profession>
        """
        print(ctx.message.server.id)
        server = ctx.message.server.id
        if ctx.invoked_subcommand is None:
            if pattern.necromancer.match(profession):
                await self.print_builds(server, "Necromancer")
                
            elif pattern.guardian.match(profession):
                await self.print_builds(server, "Guardian")
                
            elif pattern.mesmer.match(profession):
                await self.print_builds(server, "Mesmer")
                
            elif pattern.elementalist.match(profession):
                await self.print_builds(server, "Elementalist")
                
            elif pattern.warrior.match(profession):
                await self.print_builds(server, "Warrior")
                
            elif pattern.thief.match(profession):
                await self.print_builds(server, "Thief")
                
            elif pattern.revenant.match(profession):
                await self.print_builds(server, "Revenant")
                
            elif pattern.ranger.match(profession):
                await self.print_builds(server, "Ranger")
                
            elif pattern.engineer.match(profession):
                await self.print_builds(server, "Engineer")
            else:
                await self.bot.say('Invalid `builds` command passed.')
    
    @builds.command(pass_context=True)
    async def delete(self, ctx, profession, build_name):
        """
        Delete a stored build for a specific profession. Ex: ~builds delete <profession> <build name>
        """
        server = ctx.message.server.id
        if pattern.necromancer.match(profession):
            await self.delete_build(server, "Necromancer", build_name)
            
        elif pattern.guardian.match(profession):
            await self.delete_build(server, "Guardian", build_name)
            
        elif pattern.mesmer.match(profession):
            await self.delete_build(server, "Mesmer", build_name)
            
        elif pattern.elementalist.match(profession):
            await self.delete_build(server, "Elementalist", build_name)
            
        elif pattern.warrior.match(profession):
            await self.delete_build(server, "Warrior", build_name)
            
        elif pattern.thief.match(profession):
            await self.delete_build(server, "Thief", build_name)
            
        elif pattern.revenant.match(profession):
            await self.delete_build(server, "Revenant", build_name)
            
        elif pattern.ranger.match(profession):
            await self.delete_build(server, "Ranger", build_name)
            
        elif pattern.engineer.match(profession):
            await self.delete_build(server, "Engineer", build_name)
            
        else:
            await self.bot.say("update failed")
    
    @builds.group(invoke_without_command=True, pass_context=True)
    async def update(self, ctx, profession, build_name, description):
        """
        Update information for a stored build. Ex: ~builds update [description|link] <profession> <build name> <description|link>
        """
        print('In update')
        if ctx.invoked_subcommand is None:
            await self.bot.say('Invalid build command passed...')
        
    @update.command(pass_context=True)
    async def description(self, ctx, profession, build_name, description):
        """
        Update description for a stored build. Ex: ~builds update description <profession> <build name> <description>
        """
        server = ctx.message.server.id
        time = ctx.message.timestamp.strftime('%m/%d/%Y %I:%M:%S %p UTC')
        if pattern.necromancer.match(profession):
            await self.update_build(server, time, "Necromancer", build_name, description=description)
            
        elif pattern.guardian.match(profession):
            await self.update_build(server, time, "Guardian", build_name, description=description)
            
        elif pattern.mesmer.match(profession):
            await self.update_build(server, time, "Mesmer", build_name, description=description)
            
        elif pattern.elementalist.match(profession):
            await self.update_build(server, time, "Elementalist", build_name, description=description)
            
        elif pattern.warrior.match(profession):
            await self.update_build(server, time, "Warrior", build_name, description=description)
            
        elif pattern.thief.match(profession):
            await self.update_build(server, time, "Thief", build_name, description=description)
            
        elif pattern.revenant.match(profession):
            await self.update_build(server, time, "Revenant", build_name, description=description)
            
        elif pattern.ranger.match(profession):
            await self.update_build(server, time, "Ranger", build_name, description=description)
            
        elif pattern.engineer.match(profession):
            await self.update_build(server, time, "Engineer", build_name, description=description)
            
        else:
            await self.bot.say("update failed")
    
    @update.command(pass_context=True)
    async def link(self,ctx, profession, build_name, link):
        """
        Update link for a stored build. Ex: ~builds update link <profession> <build name> <link>
        """
        print('In link')
        server = ctx.message.server.id
        time = ctx.message.timestamp.strftime('%m/%d/%Y %I:%M:%S %p UTC')
        if pattern.necromancer.match(profession):
            await self.update_build(server, time, "Necromancer", build_name, link=link)
            
        elif pattern.guardian.match(profession):
            await self.update_build(server, time, "Guardian", build_name, link=link)
            
        elif pattern.mesmer.match(profession):
            await self.update_build(server, time, "Mesmer", build_name, link=link)
            
        elif pattern.elementalist.match(profession):
            await self.update_build(server, time, "Elementalist", build_name, link=link)
            
        elif pattern.warrior.match(profession):
            await self.update_build(server, time, "Warrior", build_name, link=link)
            
        elif pattern.thief.match(profession):
            await self.update_build(server, time, "Thief", build_name, link=link)
            
        elif pattern.revenant.match(profession):
            await self.update_build(server, time, "Revenant", build_name, link=link)
            
        elif pattern.ranger.match(profession):
            await self.update_build(server, time, "Ranger", build_name, link=link)
            
        elif pattern.engineer.match(profession):
            await self.update_build(server, time, "Engineer", build_name, link=link)
        else:
            await self.bot.say("update failed")
        
    @builds.command(pass_context=True)
    async def add(self, ctx, profession, build_name, description, link):
        """
        Adds new build to be stored Ex: ~builds add <profession> <build name> <description> <link>
        """
        server = ctx.message.server.id
        time = ctx.message.timestamp.strftime('%m/%d/%Y %I:%M:%S %p UTC')
        
        if pattern.necromancer.match(profession):
            await self.add_new_build(server, time, "Necromancer", build_name, description, link)
            
        elif pattern.guardian.match(profession):
            await self.add_new_build(server, time, "Guardian", build_name, description, link)
            
        elif pattern.mesmer.match(profession):
            await self.add_new_build(server, time, "Mesmer", build_name, description, link)
            
        elif pattern.elementalist.match(profession):
            await self.add_new_build(server, time, "Elementalist", build_name, description, link)
            
        elif pattern.warrior.match(profession):
            await self.add_new_build(server, time, "Warrior", build_name, description, link)
            
        elif pattern.thief.match(profession):
            await self.add_new_build(server, time, "Thief", build_name, description, link)
            
        elif pattern.revenant.match(profession):
            await self.add_new_build(server, time, "Revenant", build_name, description, link)
            
        elif pattern.ranger.match(profession):
            await self.add_new_build(server, time, "Ranger", build_name, description, link)
            
        elif pattern.engineer.match(profession):
            await self.add_new_build(server, time, "Engineer", build_name, description, link)
            
        else:
            await self.bot.say("Are you retarded? That class doesn't exist.")
    
    async def update_build(self, server, time, profession, build_name, description="", link=""):
        
        build_list = []
        found_build = False
        session = db.Session()
        results = session.query(db.Builds).filter_by(discord_server=server, profession=profession, name=build_name).one_or_none()
        
        if results:
            update_dict = {}
            if description:
                update_dict['description'] = description
                
            elif link:
                update_dict['link'] = link
            update_dict['time'] = time
            updated_build = session.query(db.Builds).filter_by(discord_server=server, profession=profession, name=build_name).update(update_dict)
            session.commit()
            msg = "Updated the " + build_name + " " + profession + " build."
            await self.bot.say(msg)
        else:
            msg = build_name + " for " + profession + " doesn't exist."
            await self.bot.say(msg) 
    
    
    async def add_new_build(self, server, time, profession, build_name, description, link):
        """
        
        """
        if not self.check_build_exists(server, profession, build_name):
            session = db.Session()
            new_build = db.Builds.__table__.insert().values(
                discord_server=server, time=time, profession=profession, name=build_name,
                description=description, link=link
            )
            session.execute(new_build)
            try:
                session.commit()
                msg = build_name + " for " + profession + " successfully added."
                await self.bot.say(msg)
            except InvalidRequestError as e:
                print(e)
                await self.bot.say("Couldn't save build. Try again")
                
        else:
            msg = build_name + " for " + profession + " already exists. You can update the build using the `~builds update` command."
            await self.bot.say(msg)
        
    def check_build_exists(self,server, profession, build_name):
        """
        
        """
        session = db.Session()
        results = session.query(db.Builds).filter_by(discord_server=server, profession=profession, name=build_name).one_or_none()
        if  results:
            return True
        return False
    
    async def print_builds(self, server, profession):
        """
        
        """
        session = db.Session()
        results = session.query(db.Builds).filter_by(discord_server=server, profession=profession).order_by(db.Builds.id)
        timestamp = datetime.datetime.now()
        if results.count() > 0:
            title = "[CALM] " + profession + " Builds"
            description = "A list of all approved " + profession + " Builds"
            embed=discord.Embed(timestamp=timestamp, title=title, description=description, color=class_colors[profession])
            for build in results:
                print(build)
                name = build.name
                value = "```" + build.description + "```Click [here](" + build.link + ") for GW2Skills.\nLast Editted: " + build.time 
                
                embed.add_field(name=name, value=value, inline=False)
            embed.set_thumbnail(url=class_thumbnails[profession])
            botmsg = await self.bot.say(embed=embed)
            await self.add_builds_reactions(botmsg, profession, server)
            
            
        else:
            title = "[CALM] " + profession + " Builds"
            description = "There are no approved " + profession + " builds currently listed."
            embed=discord.Embed(timestamp=timestamp, title=title, description=description, color=class_colors[profession])
            embed.set_thumbnail(url=class_thumbnails[profession])
            botmsg = await self.bot.say(embed=embed)
            await self.add_builds_reactions(botmsg, profession, server)
    
    async def add_builds_reactions(self, message, profession, server):
        """
        
        """
        for emoji in self.bot.profession_emojis:
            if emoji.name != profession.lower():
                await self.bot.add_reaction(message, emoji)
                
        await asyncio.sleep(0.5)
        res = await self.bot.wait_for_reaction(self.bot.profession_emojis, message=message)
        await self.print_builds(server, res.reaction.emoji.name.title())
            
    async def delete_build(self, server, profession, build_name):
        """
        
        """
        if self.check_build_exists(server, profession, build_name):
            session = db.Session()
            delete_build = session.query(db.Builds).filter_by(discord_server=server, profession=profession, name=build_name).delete()
            session.commit()
            msg = "Deleted " + build_name + " from " + profession + " build list."
            await self.bot.say(msg)
        else:
            msg = build_name + " for " + profession + " doesn't exist."
            await self.bot.say(msg)
    
    
def setup(bot):
    bot.add_cog(Builds(bot))    
    
