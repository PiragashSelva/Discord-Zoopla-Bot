# import required dependencies
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# loading the token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@client.event
async def on_ready():
    print("Success: Bot is connected!")
    print("-----------------------------------")


@client.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello, I am the Zoopla bot")


@client.command(name="goodbye")
async def goodbye(ctx):
    await ctx.send("Goodbye and take care")


@client.event
async def on_member_join(member):

    channel = client.get_channel(910874215039778902)
    await channel.send("Welcome to the server!")
    print("A member has joined")


@client.event
async def on_member_remove(member):
    channel = client.get_channel(910874215039778902)
    await channel.send("See ya chump")


client.run(TOKEN)