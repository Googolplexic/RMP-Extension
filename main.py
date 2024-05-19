# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import os
from dotenv import load_dotenv

import requests

import nextcord
from nextcord.ext import commands
import nextcord.ext
from nextcord import Intents
from nextcord import Client
from nextcord import application_command
import pickledb
from req import Player

db = pickledb.load('discord.db', True)

GUILD_ID = [1241468028378677308]

intents = Intents.default()
intents.message_content = True

bot = commands.Bot()
client = Client(intents=intents)
#tree = application_command.CommandTree(client)
#client.tree = tree
load_dotenv()

prefix = "!"
'''def get_summoner_data(summoner_name):
    url = RIOT_API_URL.replace('REGION', 'YOUR_REGION') + summoner_name
    headers = {
        'X-Riot-Token': RIOT_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
'''

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print("Ready!")

@bot.slash_command(
    name = "addtodb",
    description = "adduid",
    guild_ids= GUILD_ID
)
async def test(ctx: nextcord.Interaction, uid: str) -> None:
    author = str(ctx.user) # We get the username (RobertK#6151)
    if not db.exists(author+"apikey"): # If username is not already in the database
        db.set(author + "apikey", uid)
        await ctx.response.send_message(f'API key "{uid}" associated with "{ctx.user}" is now registered', ephemeral = True) # Make profile for username in database or it will error
    else: 
        await ctx.response.send_message(f'"{uid}" already registered with user "{ctx.user}"', ephemeral = True)

# ==============Isithas shit code begins

@bot.slash_command(
    name = "dispcurrency",
    description = "Display Currency",
    guild_ids= GUILD_ID
)
async def test(ctx: nextcord.Interaction) -> None:
    author = str(ctx.user) # We get the username (RobertK#6151)
    if not db.exists(author+"currency"): # If username is not already in the database
        await ctx.response.send_message(f'Unable to get currency associated with "{ctx.user}"', ephemeral = True) # Make profile for username in database or it will error
    else: 
        curr = db.get(author + "currency")
        await ctx.response.send_message(f'"{ctx.user}" has ${curr} in the bank', ephemeral = True)
    
# ==============Isitha's shit code ends    

class buttonMenu(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    
    @nextcord.ui.button(label = 'Accept', style=nextcord.ButtonStyle.green)
    async def confirm(self, button:nextcord.ui.Button, interaction:nextcord.Interaction):
        #this happens when it is pressed 
        await interaction.response.send_message('yes is press', ephemeral=False)
        self.value = True
        self.stop()

    @nextcord.ui.button(label = 'Decline', style=nextcord.ButtonStyle.red)
    async def deny(self, button:nextcord.ui.Button, interaction:nextcord.Interaction):
        #this happens when it is pressed 
        await interaction.response.send_message('no is press', ephemeral=False)
        self.value = True
        self.stop()

print("cheese!")
# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the
# command if it's for all guilds.
@bot.slash_command(
    name="duel",
    description="Enter an opponent's discord username to send them a duel invitation",
)
async def duel(interaction: nextcord.Interaction, opponent: nextcord.User) -> None:
    await interaction.response.send_message("Awaiting Opponent Response")
    #gets player 1
    user = await bot.fetch_user(interaction.user.id)
    #gets player 2
    print(user)
    user2 = await bot.fetch_user(opponent.id)
    print(user2)
    
    view = buttonMenu()

    await user2.send("accept or deny the duel lol", view=view)
    await view.wait()

    if view.value is None:
        return
    elif view.value:
        #do this
        print('YAH')
        print(str(user))
        #P1 = Player(str(user) + "apikey","choopedpotat", "Bruhy")
        embed = nextcord.Embed(color= 0xB9F5F1, title='LETSS GO')
        embed.add_field(name='iewruhfweiuhf',value= 'ewiufhewifhu',inline=False)
        
        await interaction.edit_original_message(content=None, embed=embed)
    #awidjaijdiawjd
    

    else:
        #do that
        print('NOH')
        
    



@bot.slash_command(
    name="cheeseinput",
    description="My first application Command",
    guild_ids = GUILD_ID
)
async def not_first_command(interaction):
    await interaction.response.send_message("cheese!")
    
@bot.slash_command(
    name = "echo",
    description = "asdw",
    guild_ids=GUILD_ID
    )
async def echo(interaction: nextcord.Interaction, message: str) -> None:
    await interaction.response.send_message(message)





@bot.slash_command(
    name="input-userid-api-id",
    description="direct messages the user and grabs a valid input",
    guild_ids=GUILD_ID
)
async def on_message(interaction):
    user = await bot.fetch_user(interaction.user.id)
    await user.send("Hello there!")
    await interaction.response.send_message("sent!")




@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == (prefix + 'changeprefix'):
        await message.channel.send('Okay! what would you like to change it to?')

    if message.content.startswith( prefix + 'hello'):
        await message.channel.send('Hello!')



try:
    token = os.getenv("TOKEN") or ""
    if token == "":
        raise Exception("The Token doesn't exist")
    bot.run(token)
except nextcord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
