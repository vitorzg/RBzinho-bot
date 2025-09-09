import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import Parameters
import Requests
import json

# Pré COnfig

load_dotenv();
discordBottoken = str(os.getenv("DISCORD_BOT_TOKEN"));
challongeToken = str(os.getenv("CHALLONGE_API_TOKEN"));
urlChallonge = "https://api.challonge.com/v1/"
intents = discord.Intents.all()
bot = commands.Bot(".", intents = intents)

# Commands

@bot.event
async def on_ready():
    print("Bot Ready")
    
# @bot.command()
# async def testy(ctx:commands.Context):
#     await ctx.reply("Testado hardware")

@bot.command()
async def listTor(ctx:commands.Context):
    
    _params = Parameters.Parameters(challongeToken) 
    torneios = Requests.api.GET(urlChallonge,"tournaments.json",_params)
    
    nomes = [t["tournament"]["name"] for t in torneios]  # type: ignore

    mensagem = "\n".join(f"- {nome}" for nome in nomes)

    await ctx.reply(f"Esses são os torneios ativos:\n{mensagem}")

bot.run(discordBottoken)