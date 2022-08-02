from io import BytesIO
import os
import discord
import requests
from database.mongodb import get_user
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # Criando comando
    @commands.command(name='profile', aliases=['card', 'p', 'perfil'])
    async def profile(self, ctx, member: discord.Member = None):
        
        # Verificando se o usuário passou um membro
        if member is None:
            user = ctx.author
        else:
            user = member

        # Verificação de cargo
        lounge = "Sem clã"
        for i in user.roles:
            if i.id == 1000805488797171782: #yakuza
                lounge = "yakuza"
            if i.id == 1001521467021873273: #Júbilo
                lounge = "Júbilo"
            if i.id == 1000926331493687326: #Erasyum
                lounge = "Erasyum"
            if i.id == 1003026320835493978: #Horcus Hand Family
                lounge = "Horcus Hand Family"

        # Verificando membros que boostaram server
        if user.id == 450011504842899459:
            background = "https://cdn.discordapp.com/attachments/1004090752567091362/1004102923195797525/FUNDOBOLINHA.png"
            color = (255, 203, 219)

        else:
            background = "https://media.discordapp.net/attachments/996464678647640264/1002659429726044190/dragao.png?width=1280&height=768"
            color = (0, 0, 0)

        # Verificação de formato de imagem
        if 'gif' in str(user.avatar_url):
            avatar = str(user.avatar_url).replace('gif', 'png')
        else:
            avatar = str(user.avatar_url)
        
        # Definições de perfil
        user = await get_user(ctx.guild.id, user.id)
        bank = user['banco']
        money = user['coins']
        lvl = user['lvl']

        # Definindo Avatar
        avatar = Image.open(BytesIO(requests.get(avatar).content))
        avatar = avatar.resize((256, 256))

        # Deixando Avatar Redondo
        bigsize = (avatar.size[0] * 3,  avatar.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)

        # Definindo fundo
        fundo = Image.open(BytesIO(requests.get(background).content))
        
        # Definindo fonte
        fonte = ImageFont.truetype('fonts/Noto.ttf', 70)

        # Definindo textos
        escrever = ImageDraw.Draw(fundo)
        escrever.text(xy=(30, 475), text=f"Clã: {lounge}", fill=color, font=fonte)
        escrever.text(xy=(20, 580), text=f"Carteira: {money}", fill=color, font=fonte)
        escrever.text(xy=(20, 685), text=f"Banco: {bank}", fill=color, font=fonte)
        escrever.text(xy=(980, 685), text=f"lvl: {lvl}", fill=color, font=fonte)

        # Colando avatar no fundo
        fundo.paste(avatar, (25, 25), avatar)

        # Salvando e enviando imagem
        fundo.save('img.png', format='PNG')
        img = discord.File(open('img.png', 'rb'))
        await ctx.send(file=img)

def setup(client):
  client.add_cog(Profile(client))
