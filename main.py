import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import Parameters
import Requests
import json
from utils.GeraId import gera_id
from utils.DateTimeConvert import convet_datetime
from datetime import datetime


# Pré COnfig

load_dotenv();
discordBotToken = str(os.getenv("DISCORD_BOT_TOKEN"));
challongeToken = str(os.getenv("CHALLONGE_API_TOKEN"));
urlChallonge = "https://api.challonge.com/v1/"
intents = discord.Intents.all()
bot = commands.Bot(".", intents = intents)

# arquivo = "data.json"

# if not os.path.exists(arquivo):
#     dados_iniciais = {}

#     with open(arquivo, "w", encoding="utf-8") as f:
#         json.dump(dados_iniciais, f, indent=4, ensure_ascii=False)

#     print(f"Arquivo '{arquivo}' criado com sucesso!")
# else:
#     print(f"Arquivo '{arquivo}' já existe.")

# Commands

@bot.event
async def on_ready():
    print("Bot Ready")
    

@bot.command()
async def rb_list(ctx:commands.Context):
    _params = Parameters.Parameters(challongeToken) 
    torneios = Requests.api.GET(urlChallonge,"tournaments.json",_params)
    nomes = [t["tournament"]["name"] for t in torneios]  # type: ignore
    mensagem = "\n".join(f"🏟️ **{nome}**" for nome in nomes)
    await ctx.reply(
        f"✨ **Torneios Ativos no Momento:** ✨\n\n"
        f"{mensagem}\n\n"
        f"🎯 Escolha o seu e prepare-se para competir! 💪🔥"
    )

@bot.command()
async def rb_create_ad(ctx:commands.Context,date_str:str,hora_str:str,rounds:int,sig_cap:int,*,name:str):
    erros = []

    if not date_str:
        erros.append("📅 **Data** é obrigatória.")
    if not hora_str:
        erros.append("⏰ **Hora** é obrigatória.")
    if not name:
        erros.append("🏆 **Nome do Torneio** é obrigatório.")
    if not isinstance(rounds, int) or rounds <= 0:
        erros.append("🔢 **Rounds** precisa ser um número maior que 0.")
    if not isinstance(sig_cap, int) or sig_cap <= 0:
        erros.append("👥 **Capacidade de Inscrição** precisa ser um número maior que 0.")
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        erros.append("📅 Data inválida. Use o formato **DD/MM/AAAA**.")

    try:
        datetime.strptime(hora_str, "%H:%M")
    except ValueError:
        erros.append("⏰ Hora inválida. Use o formato **HH:MM** (24h).")

    if erros:
        await ctx.reply(
            "⚠️ **Erro ao criar torneio:**\n" + "\n".join(f"- {e}" for e in erros)
        )
        return
    
    try:
        _params = Parameters.Parameters(challongeToken)
        _params.add_group(
            "tournament",
            open_signup=1,
            name=name,
            tournament_type="swiss",
            url=gera_id(),
            start_at=convet_datetime(data_str=date_str, hora_str=hora_str),
            swiss_rounds=rounds,
            signup_cap=sig_cap,
        )

        response = Requests.api.POST(urlChallonge, "tournaments.json", _params)

        if not response or "tournament" not in response:
            raise Exception("Resposta inválida da API")
        
        response = response["tournament"]
        link = response.get("sign_up_url", "Link não disponível")
        await ctx.reply(
            f"🎉 **Torneio Criado com Sucesso! {date_str} às {hora_str}** 🏆\n\n"
            f"🆔 **ID:** `{response.get('url', 'N/D')}`\n"
            f"🔗 **Link do Torneio:** {link}\n\n"
            f"Boa sorte aos participantes! 🍀🔥"
        )
        
    except Exception as e:
        await ctx.reply(
            "❌ **Não foi possível criar o torneio.**\n"
            "Por favor, tente novamente mais tarde ou fale com o suporte. 🛠️"
        )
        print(f"[ERRO] Falha ao criar torneio: {e}")

@bot.command()
async def rb_create_basic(ctx:commands.Context,date_str:str,hora_str:str,*,name:str):
    erros = []

    if not date_str:
        erros.append("📅 **Data** é obrigatória.")
    if not hora_str:
        erros.append("⏰ **Hora** é obrigatória.")
    if not name:
        erros.append("🏆 **Nome do Torneio** é obrigatório.")
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        erros.append("📅 Data inválida. Use o formato **DD/MM/AAAA**.")

    try:
        datetime.strptime(hora_str, "%H:%M")
    except ValueError:
        erros.append("⏰ Hora inválida. Use o formato **HH:MM** (24h).")

    if erros:
        await ctx.reply(
            "⚠️ **Erro ao criar torneio:**\n" + "\n".join(f"- {e}" for e in erros)
        )
        return
    
    try:
        _params = Parameters.Parameters(challongeToken)
        _params.add_group(
            "tournament",
            open_signup=1,
            name=name,
            tournament_type="swiss",
            url=gera_id(),
            start_at=convet_datetime(data_str=date_str, hora_str=hora_str),
            swiss_rounds=4,
            signup_cap=32,
        )

        response = Requests.api.POST(urlChallonge, "tournaments.json", _params)

        if not response or "tournament" not in response:
            raise Exception("Resposta inválida da API")
        
        response = response["tournament"]
        link = response.get("sign_up_url", "Link não disponível")
        await ctx.reply(
            f"🎉 **Torneio Criado com Sucesso! {date_str} às {hora_str}** 🏆\n\n"
            f"🆔 **ID:** `{response.get('url', 'N/D')}`\n"
            f"🔗 **Link do Torneio:** {link}\n\n"
            f"Boa sorte aos participantes! 🍀🔥"
        )
        
    except Exception as e:
        await ctx.reply(
            "❌ **Não foi possível criar o torneio.**\n"
            "Por favor, tente novamente mais tarde ou fale com o suporte. 🛠️"
        )
        print(f"[ERRO] Falha ao criar torneio: {e}")

bot.run(discordBotToken)