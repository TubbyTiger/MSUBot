import discord
from discord.ext import commands
import subprocess
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass


bot = commands.Bot(command_prefix='!', description='Set roles & more to come.')
self_name = "MSUBot"
user = input('Username:')
pswd = getpass.getpass('Password:')


def netid_search(user,pswd,netid):

    driver = webdriver.Firefox()
    driver.get("https://search.msu.edu/people/index.php")
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'msu-id'))).send_keys(user)
    driver.find_element_by_id("password").send_keys(pswd)
    driver.find_element_by_name("submit").click()
    print("authenticated")
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'nid'))).send_keys(netid)
    driver.find_element_by_name("submit").click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'maincontent'))).click()
    title = driver.find_element_by_class_name("title").text.replace("TITLE:","").strip()
    status = driver.find_element_by_class_name("classdesc").text.replace("STATUS:","").strip()
    major = driver.find_element_by_class_name("majordesc").text.replace("MAJOR:","").strip()
    driver.close()
    return title,status,major


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
    server_roles = list(map(str,message.server.roles))
    if split_msg[0] == "!netid":
        await bot.send_message(message.channel, "Searching......")
        major = netid_search(user,pswd,split_msg[1])[2]
        role = discord.utils.get(message.server.roles, name=major)
        #if there is already a role in the server
        if major in server_roles:
            #if the user already has that role
            if major in message.author.roles:
                await bot.send_message(message.channel, "You already have the role: "+major)
            else:
                await bot.add_roles(message.author, role)
                await bot.send_message(message.channel,"Your role: "+major+" has been added")
        else:
            await bot.create_role(message.server,name=major)
            await bot.send_message(message.channel, "Role: "+major+" created")
            #NEED TO REDECLARE ROLE
            role = discord.utils.get(message.server.roles, name=major)
            await bot.add_roles(message.author, role)
            await bot.send_message(message.channel, "Your role: " + major + " has been added")



'''
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
'''






bot.run("")
