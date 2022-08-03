import asyncio
import random

import discord
from database.mongodb import checkMoney, lvlGalo, update_user, user_get
from discord.ext import commands

atack = ['atacou por trás do', 'atacou por frente do', 'atacou por cima do', 'acertou a cabeça do', 'acertou as costas do']
critical = ['quebrou uma perna do', 'rasgou o peito do', 'depenou o pescoço do']
dodge = ['desviou pela direita do', 'deu um pulo e saiu ileso do', 'desviou com classe do']
block = ['bloqueou o ataque do', 'segurou o ataque do', 'aguentou com as asas o ataque do']
class Galo(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command()
    async def rinhas(self, ctx):
        
        galos = ['**1️⃣ GALO: João sem braço**', '**2️⃣ GALO: Zézinho**', '**3️⃣ GALO: Ricardo pé de ferro**', '**4️⃣ GALO: Galo de pedra**']
        vidas = [95, 100, 150, 500]
        forcas = [25, 30, 50, 150]
        valores = [250, 300, 500, 1000]
        var_xps = [5, 10, 25, 50]

        embed = discord.Embed(title="Rinhas", description=f"** **", color=0x4FABF7)
        for galo, vida, forca, valor, var_xp in zip(galos, vidas, forcas, valores, var_xps):
            embed.add_field(name=f"{galo}", value=f"``Fácil``", inline=False)
            embed.add_field(name="**Vida**", value=f"{vida}", inline=False)
            embed.add_field(name="**Força**", value=f"{forca}", inline=False)
            embed.add_field(name="**Valor**", value=f"{valor}", inline=False)
            embed.add_field(name="**XP**", value=f"{var_xp}", inline=False)
        msg = await ctx.send(embed=embed)

        # Adicionando reações
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        for i in reactions:
            await msg.add_reaction(i)

        # Função de verificação das reações
        def check(reaction, user):
            return user.id == ctx.author.id and str(reaction.emoji) in reactions

        # Esperando por reações
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=20.0, check=check)

            # Definindo reações e escolhas
            escolhas = reactions
            names = ['João sem braço', 'Zézinho', 'Ricardo pé de ferro', 'Galo de pedra']
            lifes = [95, 100, 150, 500]
            forces = [25, 30, 50, 150]
            prices = [250, 300, 500, 1000]
            xps = [5, 10, 25, 50]
            
            for escolha, name, life, force, price, xp in zip(escolhas, names, lifes, forces, prices, xps):
                if str(reaction.emoji) == escolha:

                    if not await checkMoney(ctx.guild.id, ctx.author.id, price):
                        await ctx.send(f'@{ctx.author.name}, @{ctx.author.name} não possui coins suficientes na carteira.')
                        return
                    # Criando galo
                    galo2 = {'nome': name, 'vida': life, 'dano': force, 'dodge': 10, 'block': 40, 'crit': 30}
                    xp_a_ganhar = xp
                    price_a_ganhar = price
                    galo1 = await user_get(ctx.guild.id, ctx.author.id, 'galo')

            # Criando embed
            embed = discord.Embed(title="Rinha de galo", value=f"{galo2['nome']} vs {galo2['nome']}", color=0x4FABF7)
            embed.add_field(name="**Começando**", value=f"** **", inline=False)

            log = discord.Embed(title="Log da rinha", value=f"{galo1['nome']} vs {galo2['nome']}", color=0x4FABF7)
            msg = await ctx.channel.send(embed=embed)
            turns = 0

            while True:
                if turns % 2 == 0:
                    atackerName = ctx.author.name
                    atacker = galo1
                    defenderName = galo2['nome']
                    defender = galo2

                else:
                    atackerName = galo2['nome']
                    atacker = galo2     
                    defenderName = ctx.author.name
                    defender= galo1

                
                if random.randint(1, 100) <= defender['dodge']:
                        log.add_field(name=f"turno {turns}", value=f"``{defender['nome']} {random.choice(dodge)} {atacker['nome']}``", inline=False)
                        turns += 1
                
                elif random.randint(1, 100) <= atacker['crit']:
                        if random.randint(1,100) <= defender['block']:
                            log.add_field(name=f"turno {turns}", value=f"``{defender['nome']} segurou um ataque critico do {atacker['nome']} , recebendo {atacker['dano']} de dano``", inline=False)
                            defender['vida'] -= atacker['dano']
                            log.add_field(name=f"``{galo1['nome']}: {galo1['vida']} de vida``", value=f"** **", inline=False)
                            log.add_field(name=f"``{galo2['nome']}: {galo2['vida']} de vida``", value=f"** **", inline=False)
                            turns += 1
                        else:
                            log.add_field(name=f"turno {turns}", value=f"``{atacker['nome']} {random.choice(critical)} {defender['nome']}, dando {atacker['dano'] * 2} de dano``", inline=False)
                            defender['vida'] -= atacker['dano'] * 2
                            log.add_field(name=f"``{galo1['nome']}: {galo1['vida']} de vida``", value=f"** **", inline=False)
                            log.add_field(name=f"``{galo2['nome']}: {galo2['vida']} de vida``", value=f"** **", inline=False) 
                            turns += 1
                        
                elif random.randint(1, 100) <= defender['block']:
                        log.add_field(name=f"turno {turns}", value=f"``{defender['nome']} {random.choice(block)} {atacker['nome']}, recebendo {round(atacker['dano'] / 2)} de dano``", inline=False)
                        defender['vida'] -= round(atacker['dano'] / 2)
                        log.add_field(name=f"``{galo1['nome']}: {galo1['vida']} de vida``", value=f"** **", inline=False)
                        log.add_field(name=f"``{galo2['nome']}: {galo2['vida']} de vida``", value=f"** **", inline=False) 
                        turns += 1  
                else:
                    log.add_field(name=f"turno {turns}", value=f"``{atacker['nome']} {random.choice(atack)} {defender['nome']}, recebendo {atacker['dano']} de dano``", inline=False)
                    defender['vida'] -= atacker['dano']
                    log.add_field(name=f"``{galo1['nome']}: {galo1['vida']} de vida``", value=f"** **", inline=False)
                    log.add_field(name=f"``{galo2['nome']}: {galo2['vida']} de vida``", value=f"** **", inline=False) 
                    turns += 1  

                if defender['vida'] <= 0:
                    if defender == galo1:
                        embed = discord.Embed(title="Rinha de galo", value=f"** **", color=0x4FABF7)
                        embed.add_field(name="**Fim**", value=f"``{atackerName} venceu a rinha de galo com {defenderName}``", inline=False)
                        await ctx.send(embed=log)
                        await ctx.send(embed=embed) 
                        return
                    else: 
                        coins = await user_get(ctx.guild.id, ctx.author.id, 'coins')
                        coinsdown = coins - price_a_ganhar
                        coinsup = coins + price_a_ganhar + 50
                        embed = discord.Embed(title="Rinha de galo", value=f"** **", color=0x4FABF7)
                        embed.add_field(name="**Fim**", value=f"``{atackerName} venceu a rinha de galo com {defenderName}``", inline=False)
                        embed.add_field(name="**XP de galo adquirido**", value=f"``{xp_a_ganhar}``", inline=False)
                        embed.add_field(name="**Valor recebido por vitória: **", value=f"``{price_a_ganhar + 50}``", inline=False)
            
                        await ctx.send(embed=log)
                        await ctx.send(embed=embed)
                        coins = await user_get(ctx.guild.id, ctx.author.id, 'coins')
                        coinsdown = coins - price_a_ganhar
                        coinsup = coins + price_a_ganhar + 50

                        await update_user(ctx.guild.id, ctx.author.id, 'coins', coinsdown, 'set')
                        await lvlGalo(ctx.guild.id, ctx.author.id, xp_a_ganhar)
                        await update_user(ctx.guild.id, ctx.author.id, 'coins', coinsup, 'set')
                        return
        # Deletando a mensagem caso user não inserir uma reação
        except asyncio.TimeoutError:
            return await msg.delete()
        # Função de verificação das reações

def setup(client):
    client.add_cog(Galo(client))
