import discord
from discord.ext import commands
import subprocess

bot = commands.Bot(command_prefix='!', description='Set roles & more to come.')
self_name = "MSUBot"
class_ranks = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Alumni']

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')

@bot.command()
async def cowsay(msg:str):
    msg = subprocess.check_output(['cowsay', msg]).decode('utf-8')
    await bot.say('```' + msg + '```')

@bot.event
async def on_message(message):
    split_msg = message.content.split()
    rank = split_msg[2].lower().title()
    server = message.server
    role = discord.utils.get(server.roles, name=rank)
    has_role = False

    if not message.author.name == self_name:
        # Set class rank
        if split_msg[0] == "!set":
            if split_msg[1] == 'grade' :
                for roles in message.author.roles:
                    print(roles)
                    if str(roles) in class_ranks:
                        print("HAVE ROLE")
                        has_role = True
                        await bot.send_message(message.channel, "You already have a role.")
                        break
                if has_role == False:
                    await bot.add_roles(message.author, role)
                    await bot.send_message(message.channel, "Role was added.")
bot.run()
