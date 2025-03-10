import disnake
from replit import db
from disnake.ext import commands
import random
import asyncio
import requests
import json
import time
import os
apikey = os.environ['perapi']

from pyspective import pyspective

perspective = pyspective.PyspectiveAPI(apikey)

cashE = '<:YeetCoin:899166414546559056>'

class SlashCommands(commands.Cog, name='Slash commands'):
    '''These are the slash commands'''
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name='nsfw',description="It's not")
    async def nsfw(self, inter):
      await inter.response.send_message('https://tenor.com/view/rick-astly-rick-rolled-gif-22755440')

    #economy
    global cashE

    @commands.slash_command(name='cash',description='Your cash')
    async def cash(self, inter,user:disnake.Member=None):
      if user is None:
        try:
          value = db[f'{inter.author.id}']
          await inter.response.send_message(f'You currently have {value} {cashE}')
        except KeyError:
          value = db[inter.author.id]='0'
          await inter.response.send_message(f'You currently have {value} {cashE}')
      else:
        try:
          value = db[f'{user.id}']
          await inter.response.send_message(f'{user.mention} currently have {value} {cashE}')
        except KeyError:
          value = db[f'{user.id}']='0'
          await inter.response.send_message(f'{user.mention} currently have {value} {cashE}')

      
    @commands.slash_command(name='work',description='Work to get more coins')
    @commands.cooldown(rate=1, per=600)
    async def work(self, inter):
      e = random.randint(-250,250)
      try:
        value = int(db[f'{inter.author.id}'])
        value += e
        db[f'{inter.author.id}'] = f'{value}'
        if e<0:
          await inter.response.send_message(f'You messed things up! You spend {-e}{cashE} to make things back.')
        elif e>=0 and e<=50:
          await inter.response.send_message(f"What a lazy guy. You didn't work enough. That is why you only get {e}{cashE}.")
        else:
          await inter.response.send_message(f'You did a great job. You get {e}{cashE} for that.')
      except KeyError:
        db[inter.author.id]=f'{e}'
        if e<0:
          await inter.response.send_message(f'You messed things up! You spend {-e}{cashE} to make things back.')
        elif e<=0 and e<50:
          await inter.response.send_message(f"What a lazy guy. You didn't work enough. That is why you only get {e}{cashE}.")
        else:
          await inter.response.send_message(f'You did a great job. You get {e}{cashE} for that.')

      
    @commands.slash_command(name='transfer',description='Give someone your cash with a little tax')
    async def give(self, inter,user:disnake.User,cash:int):
      try:
        value1 = int(db[f'{inter.author.id}'])
        value2 = int(db[f'{user.id}'])
        if value1 > cash:
          e=cash/100*80
          value1 -= cash
          db[f'{inter.author.id}'] = f'{value1}'
          value2 += e
          db[f'{user.id}'] = f'{value2}'
          await inter.response.send_message(f'You gave {e} to  {user.mention} after 20% tax. Now, you have {value1} and they got {value2}.')
        else:
          await inter.response.send_message("You don't have enough cash to do it.")
      except KeyError:
        db[f'{user.id}'] = '0'
        value1 = int(db[f'{inter.author.id}'])
        value2 = int(db[f'{user.id}'])
        if value1 > cash:
          e=cash/100*80
          value1 -= cash
          db[f'{inter.author.id}'] = f'{value1}'
          value2 += e
          db[f'{user.id}'] = f'{value2}'
          await inter.response.send_message(f'You gave {e} to  {user.mention} after 20% tax. Now, you have {value1} and they got {value2}.')

        else:
          await inter.response.send_message("You don't have enough cash to do it.")

      
    @commands.slash_command(name='test')
    async def test(self, inter):
      if inter.author.id == 832264231617167381 or inter.author.id == 543656290468102174:
        E = db[f'{inter.author.id}']
        e = int(E)
        e += 50000
        db[f'{inter.author.id}'] = f'{e}'
        await inter.response.send_message('Dev powah >:)')

    
    @commands.slash_command(name='clear')
    async def clear(self, inter,user:disnake.User):
      if inter.author.id == 832264231617167381 or inter.author.id == 543656290468102174:
        db[f'{inter.author.id}'] = '0'
        await inter.response.send_message('Dev powah >>:)')


    @commands.slash_command(name='leaderboard',description='Show the top 20 richest users')
    async def lb(self, inter):
      e = {}
      high = {}
      for x in inter.guild.members:
        try:
          e.update({x.name: int(db[str(x.id)])})
        except KeyError:
          db[f"{x.id}"]='0'
          e.update({x.name: 0})
      high=dict(sorted(e.items(),key= lambda x:x[1], reverse = True))
      text = ''
      e = 0
      for x in high:
        if e == 20:
          return
        else:
          text += f'{x}: {high[x]}\n'
        e+=1
      embed = disnake.Embed(title=f'Top highest in {inter.guild.name}',description=text,color=0x6ba4ff)
      await inter.response.send_message(embed=embed)

    #Giveaway

    @commands.slash_command(name='create_giveaway')
    @commands.has_permissions(manage_guild=True)
    async def cgw(self, inter,times:int,winners,*,prize):
      eh = time.time()
      x=0
      for x in range(0,times):
        eh+=1
        x+=1
      eh=int(eh)
      print(x)
      embed=disnake.Embed()
      embed.add_field(name=prize,value=f'React with 🎉 to enter!\nTime: <t:{eh}:R>\nHosted by: {inter.author.mention}')
      embed.set_footer(text = f'{winners} winner(s)')
      gwlink = await inter.response.send_message(embed=embed)
      await gwlink.add_reaction('🎉')
      await asyncio.sleep(x)
      for s in gwlink.reactions:
        if s.emoji.name == "tada":
          users = await s.users().flatten()
          winner = random.choice(users)
          await gwlink.channel.response.send_message(f'{winner.mention} has won the raffle.')

    #Mod 

    @commands.slash_command(name='ban',description='Ban user')
    @commands.has_permissions(ban_members=True)
    async def ban(self, inter, user: disnake.Member, *, reason=None):

        await inter.response.send_message(f'{user.mention} was banned. Reason: {reason}')
        await inter.guild.ban(user, reason=reason)

    @commands.slash_command(name='kick',description='Kick user')
    @commands.has_permissions(kick_members=True)
    async def kick(self, inter, user: disnake.Member, *, reason=None):

        await inter.guild.kick(user, reason=reason)
        await user.response.send_message(
            f'You got banned from {user.guild.name}. Reason:{reason} ')
        await inter.response.send_message(f'{user.mention} was banned. Reason: ')

    @commands.slash_command(name='ban_list',description='Get the banned users list')
    @commands.has_permissions(ban_members=True)
    async def banList(self, inter):

        embed = disnake.Embed(title=f'Banned user in {inter.guild.name}')
        bans = await inter.guild.bans()
        for x in bans:
            embed.add_field(
                name=
                f'User {x.user.name}#{x.user.discriminator} with ID: {x.user.id}',
                value=f'Reason: {x.reason}')
        await inter.author.response.send_message(embed=embed)
        await inter.response.send_message('Sent. Check your DM')

    @commands.slash_command(name='unban',description='Unban user')
    @commands.has_permissions(ban_members=True)
    async def unban(self, inter, *, userid):
        userid = int(userid)
        user = await self.bot.fetch_user(userid)
        await inter.guild.unban(user)
        await inter.response.send_message(f'{user.mention} is unbanned!')

    @commands.slash_command(name='nuke', description='Clone and delete a channel')
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, inter):
        m = inter.channel.position
        e = await inter.channel.clone()
        await inter.channel.delete()
        await e.edit(position=m)
        await e.response.send_message(f'{inter.message.author.mention} nuked the channel')

    @commands.slash_command(name='check_toxicity',description='Check the toxicity of a word/sentence')
    async def ct(self, inter, *, other):
        scores = perspective.score(other)
        My_Attribute = scores["TOXICITY"]
        await inter.response.send_message(
            f"Toxicity test for {other} completed.\nIt's toxicity is {My_Attribute.score*100}"
        )

    @commands.slash_command(name='mute', description='Mute user')
    @commands.has_permissions(manage_messages=True)
    async def mute(self, inter, user: disnake.Member, *, reson=None):

        overwrite = disnake.PermissionOverwrite()
        overwrite.response.send_message_messages = False
        overwrite.read_messages = True
        breh = disnake.utils.get(inter.guild.roles, name="Muted by YAIS")
        if breh == None:
            await inter.guild.create_role(name="Muted by YAIS")
            await self.bot.add_roles(member=user, role=breh)
            for x in inter.guild.text_channels:
                await x.set_permissions(breh, overwrite=overwrite)
                await inter.response.send_message('Muted')
        else:
            await user.add_roles(breh)
            for x in inter.guild.text_channels:
                await x.set_permissions(breh, overwrite=overwrite)
        await inter.response.send_message(f'User {user} has been muted. Reason: {reson}')

    @commands.slash_command(name='unmute',description='Unmute user')
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, inter, user: disnake.Member, *, reson=None):

        overwrite = disnake.PermissionOverwrite()
        overwrite.response.send_message_messages = False
        overwrite.read_messages = True
        breh = disnake.utils.get(inter.guild.roles, name="Muted by YAIS")
        if breh == None:
            await inter.guild.create_role(name="Muted by YAIS")
            await self.bot.remove_roles(member=user, role=breh)
            for x in inter.guild.text_channels:
                await x.set_permissions(breh, overwrite=overwrite)
                await inter.response.send_message('Muted')
        else:
            await user.remove_roles(breh)
            for x in inter.guild.text_channels:
                await x.set_permissions(breh, overwrite=overwrite)
        await inter.response.send_message(f'User {user} has been unmuted. Reason: {reson}')

    @commands.slash_command(name='purge', description='Delete a number of messages')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, inter, count: int):

        count += 1
        deleted = await inter.channel.purge(limit=count)
        await inter.response.send_message(f'Deleted {len(deleted)-1} message', delete_after=3)

    @commands.slash_command(name='role',description='Give/remove role from an user')
    @commands.has_permissions(manage_roles=True)
    async def role(self, inter, user: disnake.Member, role: disnake.Role):

        if role in user.roles:
            await user.remove_roles(role)
            await inter.response.send_message(
                f'Successfully removed {user.mention} {role.mention}')
        else:
            await user.add_roles(role)
            await inter.response.send_message(f'Successfully added {user.mention} {role.mention}')

    @commands.slash_command(name='is_scammer',description='Check is a user a scammer. Not always true')
    async def isScammer(self, inter, user: disnake.User):
        r = requests.get(
            f"https://disnakescammers.com/api/v1/search/{user.id}",
            verify=False)
        response = r.json()
        print(response['status'])
        if response['status'] == 'not_found':
            await inter.response.send_message('That user **might** not a scammer.')
        else:
            await inter.response.send_message('That user is a scammer.')

    @commands.slash_command(name='report_scammer',description='Report scammer')
    async def reportScammer(self, inter, user: disnake.User, *, info):
        daata = {
            'ScammerID': f"{user.id}",
            'ScammerUsername': f"{user.name}",
            'AdditionalInfo': info
        }
        postME = json.dumps(daata)
        requests.post('https://disnakescammers.com/api/v1/report',
                      data=postME,
                      verify=False)
        await inter.response.send_message('Reported!')

    #Suggest

    @commands.slash_command(name='suggest', description='Suggest a idea')
    async def suggest(self, inter,*,idea):
        embedVar = disnake.Embed(title=f"Suggest from user with ID: {inter.author.id}", description=f'{idea}', color=0x6FB9FF)
        with open('cogs/isban.txt')as file:
          for isBanned in file:
            isBanned = int(isBanned)
            if inter.author.id != isBanned:
              with open('cogs/channel.txt')as f:
                  for hey in f:
                    hey=int(hey)
                    channel = inter.guild.get_channel(hey)
                    if channel is not None:
                      hmm = await channel.response.send_message(content=inter.author.id,embed=embedVar)
                      cross = '\N{THUMBS DOWN SIGN}'
                      checkM = '\N{THUMBS UP SIGN}'
                      await hmm.add_reaction(checkM)
                      await hmm.add_reaction(cross)
              embedBreh = disnake.Embed(title='Sent',value='Your suggestion has been sent!')
              await inter.response.send_message(embed=embedBreh)
            else:
              inter.response.send_message("You have been banned from our system.")
              return 0
    @commands.slash_command(name='approve', description='Approve a suggestion')
    @commands.has_permissions(manage_messages=True)
    async def _approve(self, inter,id):
        id=int(id)
        global yay
        huh = await inter.channel.fetch_message(id)
        member = huh.content
        member = int(member)
        user = await inter.bot.fetch_user(member)
        await huh.response.send_message(f'Suggest is approved!')
        await huh.edit(content=f'{user.mention} Your suggest has been approved!')
        

    @commands.slash_command(name='decline', description='Decline a suggestion',)
    @commands.has_permissions(manage_messages=True)
    async def _decline(self, inter,id):
        id=int(id)
        global yay
        huh = await inter.fetch_message(id)
        await huh.response.send_message(f'{huh.author.mention} Your suggest has been declined!')
        await huh.edit(content='Declined.')

  

    @commands.slash_command(name='setup', description='Set up channel that suggestions will be sent to it')
    @commands.has_permissions(manage_channels=True)
    async def _setup(self, inter,id=None):
        if id is None:
            with open('cogs/channel.txt','a') as f:
                f.write('\n')
                f.write(str(inter.channel.id))
        else:
            with open('cogs/channel.txt','a') as f:
                f.write('\n')
                f.write(id)
        embedVar = disnake.Embed(title="Set up done!",color=0x85C4FF)
        await inter.response.send_message(embed=embedVar)

    @commands.slash_command(name='report',description='Report a suggestion')
    async def _report(self, inter,messagelink):
        re = await inter.bot.fetch_channel(883956344472895529)
        await re.response.send_message(content=messagelink)
        await inter.response.send_message(content='Sent')

def setup(bot):
    bot.add_cog(SlashCommands(bot))