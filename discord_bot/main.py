
from random import randint
import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
from bs4 import BeautifulSoup
from googletrans import Translator
from config import settings
import json
import requests

# client = discord.Client()
client = commands.Bot(command_prefix='!')

slashs = SlashCommand(client, sync_commands=True)

async def create_voice_channel(category, channel_name):
    channel = await category.create_voice_channel(channel_name)
    return channel

async def delete_channel(guild, channel_id):
    channel = guild.get_channel(channel_id)
    await channel.delete()

@client.command()

class PythonJokes:

    def __init__(self):
        self.url = 'https://www.anekdot.ru/random/anekdot/'
        self.html = self.get_html()

    def get_html(self):
        try:
            result = requests.get(self.url)
            result.raise_for_status()
            return result.text
        except(requests.RequestException, ValueError):
            print('Server error')
            return False

    def get_jokes(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        news_list = soup.findAll('div', class_='text')
        return news_list


@client.event
async def on_ready():
    DiscordComponents(client)
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return

    if ctx.content.startswith('$hello'):
        client_id = ctx.author.mention
        await ctx.channel.send(f'Салам, {client_id} ')

    if ctx.content.startswith('$embed'):
        ctx.clean_content
        embed = discord.Embed(title="Презентация бота", url="https://realdrewdata.medium.com/",
                              description="Все аргументы и причины, почему этот бот классный",
                              color=discord.Colour.red())
        embed.set_thumbnail(
            url="https://w7.pngwing.com/pngs/627/370/png-transparent-christmas-gift-gifts-to-send-non-stop-miscellaneous-ribbon-wedding.png")
        embed.add_field(name='Первая причина', value="Он создает прикольные постеры", inline=True)
        embed.add_field(name='Вторая причина', value="Он крут", inline=True)
        embed.add_field(name='Третья причина', value="Я так сказал", inline=False)
        await ctx.channel.send(embed=embed)
        await ctx.delete()

    if ctx.content.startswith('$fox'):
        response = requests.get('https://some-random-api.ml/animal/fox?image')  # Get-запрос
        json_data = json.loads(response.text)  # Извлекаем JSON
        translator = Translator()
        fact = translator.translate(json_data['fact'], dest='ru', src='en')
        embed = discord.Embed(color=0xff9900, title='Random Fox')  # Создание Embed'a
        embed.set_image(url=json_data['image'])  # Устанавливаем картинку Embed'a
        embed.add_field(name='**Интересный факт**', value=fact.text, inline=False)
        await ctx.channel.send(embed=embed)  # Отправляем Embed


@slashs.slash(name='hi', description='Приветствие', guild_ids=[727593198125580291],
              options=[{'name': 'member', 'description': 'пользователь', 'type': 6, 'required': True}])
@client.command()
async def hi(ctx, member: discord.member = None):
    await ctx.send(f'Передаю привет {member.mention}!')


@slashs.slash(name='joke', description='Анекдот', guild_ids=[727593198125580291])
async def joke(ctx):
    joke = PythonJokes()
    author = ctx.author.mention
    result_joke = str(joke.get_jokes()[0]).split('<div class="text">')[-1]
    result_joke = "\n".join(result_joke.split("<br/>"))[0:-6]
    embed1 = discord.Embed(title="**Анекдот по запросу:**", url="",
                           description=result_joke,
                           color=discord.Colour.blue())
    embed1.set_thumbnail(
        url=ctx.author.avatar_url)
    embed1.add_field(name='**Запросил: **', value=author, inline=True)
    await ctx.send(embed=embed1)


@slashs.slash(name='duel', description='Сразиться', guild_ids=[727593198125580291],
              options=[{'name': 'member', 'description': 'пользователь', 'type': 6, 'required': True}])
async def duel(ctx, member: discord.member = None):
    await ctx.send(embed=discord.Embed(title='Дуэль'),
                   components=[
                       Button(style=ButtonStyle.blue, label='Принять'), Button(style=ButtonStyle.red, label='Отклонить')
                   ])

    msg = await ctx.channel.history().get(author__id=903930612518383626)
    response = await client.wait_for('button_click')
    await msg.delete(delay=1)
    if response.channel == ctx.channel:
        if response.component.label == 'Принять':
            winner = randint(0, 1)
            if winner == 0:
                embed12 = discord.Embed(title='Дуэль')
                embed12.add_field(name='Победитель:', value=member, inline=False)
                await ctx.send(content="Победил " + member.mention)
            else:
                embed13 = discord.Embed(title='Дуэль')
                embed13.add_field(name='Победитель:', value=ctx.author, inline=False)
                await ctx.send(content="Победил " + ctx.author.mention)

client.run(settings['token'])
