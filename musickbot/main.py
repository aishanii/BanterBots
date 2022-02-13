import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import music

cogs = [music]


client = commands.Bot(command_prefix='|', intents = discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)




client.run("OTQyMTI3MTIzMzUzNzAyNDYy.Ygf-Qg.JJBBwA4iX_0PorDO7Mb7QNw5RR0")