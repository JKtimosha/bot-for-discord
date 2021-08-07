import discord
import asyncio
import os
import random
import io
import re
import json
import requests
import contextlib

from discord_components import DiscordComponents, Button, ButtonStyle
from discord.ext import commands

statuss_type_array = ['playing', 'watching', 'listening', 'competing', 'streaming']

async def playing(statuss):
	await client.change_presence(status = discord.Status.dnd, activity = discord.Game(f'{statuss}'))
async def streaming(statuss):
	await client.change_presence(status = discord.Status.dnd, activity = discord.Streaming(name=f'{statuss}', url='https://twitch.tv/pewdiepie'))
async def watching(statuss):
	await client.change_presence(status = discord.Status.dnd, activity = discord.Activity(type=discord.ActivityType.watching, name = f'{statuss}'))
async def listening(statuss):
	await client.change_presence(status = discord.Status.dnd, activity = discord.Activity(type=discord.ActivityType.listening, name = f'{statuss}'))
async def competing(statuss):
	await client.change_presence(status = discord.Status.dnd, activity = discord.Activity(type=discord.ActivityType.competing, name = f'{statuss}'))

client = commands.Bot(command_prefix = '!')

server_id = 859784071046627388
role1 = 859787450959396865
role2 = 859786838109978625
role3 = 859795332631363585
admins_id = [690149608403370032, 610453921726595082, 847387836432384021]

with open('statuses.txt', encoding='utf-8') as f:
	statuses_array = f.readlines()

async def status():
	while True:
		statuss_name = random.choice(statuses_array)
		statuss_type = random.choice(statuss_type_array)
		if statuss_type == 'playing':
			await playing(statuss_name)
		elif statuss_type == 'streaming':
			await streaming(statuss_name)
		elif statuss_type == 'watching':
			await watching(statuss_name)
		elif statuss_type == 'listening':
			await listening(statuss_name)
		else:
			await competing(statuss_name)
		await asyncio.sleep(5.5)

@client.event
async def on_ready():
	DiscordComponents(client)
	client.loop.create_task(status())
	print('bot ready to ebat\'')

@client.event
async def on_member_remove(member):
	jsonn = {
  "content": None,
  "embeds": [
    {
      "title": "Аватарка пидора:",
      "color": 65280,
      "thumbnail": {
        "url": f"{member.avatar_url}"
      }
    },
    {
      "title": "Ещё одна падла вышла!",
      "description": "Эта падла вышла и я её отпиздил молотком по еблу(забанил). Если вы не хотите оказаться в её положении, пж не уходите((((",
      "color": 65280,
      "fields": [
        {
          "name": "Имя падлы:",
          "value": f"{member.name}#{member.discriminator}",
          "inline": True
        },
        {
          "name": "ID падлы:",
          "value": f"{member.id}",
          "inline": True
        }
      ],
      "footer": {
        "text": "С любовью, Dungeon Master, JKCrashers🥰💖"
      },
      "image": {
        "url": "https://cdn.discordapp.com/attachments/862274574280032276/864162952764063774/16224779837650.png"
      }
    }
  ]
}
	try:
		await member.ban()
		requests.post('вебхук', json = jsonn)
	except:
		pass

@client.command(aliases=['выебать'])
async def command(ctx, *, user: discord.Member=None):
	server = discord.utils.get(client.guilds, id=server_id)
	access_role = discord.utils.get(server.roles, name='〘.!.〙доступ к !выебать')
	if access_role in ctx.author.roles:
		server = discord.utils.get(client.guilds, id=server_id)
		role11 = discord.utils.get(server.roles, name='〘.!.〙Мать в канаве')
		role22 = discord.utils.get(server.roles, name='〘.!.〙Долбаеб')
		role33 = discord.utils.get(server.roles, name='〘.!.〙был выебан админами')
		if user:
			if user.id != client.user.id:
				try:
					await user.add_roles(role11)
					await user.add_roles(role22)
					await user.add_roles(role33)
				except:
					await ctx.send(f'{ctx.author.mention}, пользователя нет на сервере.')
				if role33 in user.roles:
					await ctx.send(f'<@!{user.id}>(уже был выебан до этого), хорошего тебе дня, пупсик :)))))))))))))')
				else:
					await ctx.send(f'<@!{user.id}>(не был выебан), хорошего тебе дня, пупсик :)))))))))))))')
			else:
				await ctx.send('не пытайся выебать меня....')
		else:
			await ctx.send('Сначала надо ползователя пингануть окда.')
	else:
		await ctx.send('а вот хуй тебе :)))))))')

@command.error
async def command2_error(error):
	if isinstance(error, commands.errors.MemberNotFound):
	  await ctx.send(f'{ctx.author.mention}, пользователя нет на сервере.')
	else:
	  pass

@client.command(aliases=['start'])
async def yt(ctx):
	try:
		channel = ctx.author.voice.channel
		url = f"https://discord.com/api/v9/channels/{channel.id}/invites"
		params = {
									'max_age': 0,
									'max_uses': 0,
									'target_application_id': '755600276941176913', 
									'target_type': 2,
									'temporary': False,
									'validate': None
								}
		headers={'content-type': 'application/json','Authorization': f"Bot токен"}
		r=requests.post(url, data=json.dumps(params), headers=headers)
		
		buttons = [Button(style = ButtonStyle.URL, url = f"https://discord.gg/{r.json()['code']}", label = 'Начать просмотр(только с пк)')]
		embed = discord.Embed(title = 'YouTube прямо в голосовом чате дискорд!', description = 'Я добавил новую систему кнопок, чтобы вам было проще, они находятся ниже.\nЕсли вы их не видите, обновите дискорд.\nРекомендую закрепить это сообщение, т.к сссылка будет работать даже если бот выключен, и она бесконечная!', color = 0xFF1D1D)
		await ctx.send(embed = embed, components = buttons)
	except AttributeError as e:
		await ctx.send("Подключись к любому голосовому чату, чтобы продолжить.")
		print(e)
	except Exception as e:
		print(e)
		await ctx.send("При запуске Youtube Togther произошла ошибка, или у меня нет разрешения на создание приглашений.")

@client.command(aliases=['чекнуть', 'чек', 'проверить', 'выебан-ли'])
async def __command2(ctx, *, user: discord.Member=None):
	server = discord.utils.get(client.guilds, id=server_id)
	role11 = discord.utils.get(server.roles, name='〘.!.〙Мать в канаве')
	role22 = discord.utils.get(server.roles, name='〘.!.〙Долбаеб')
	role33 = discord.utils.get(server.roles, name='〘.!.〙был выебан админами')
	roles1 = [role11, role22]
	roles2 = [role11, role22, role33]
	try:
		if user:
			if role11 in user.roles:
				await ctx.send(f'{ctx.author.mention}, {user.mention} сейчас выебан.')
			elif role33 in user.roles:
				if roles1 not in user.roles:
					await ctx.send(f'{ctx.author.mention}, {user.mention} сейчас не выебан, но был выебан ранее.')
			else:
				await ctx.send(f'{ctx.author.mention}, {user.mention} сейчас не выебан, и не был выебан ранее.')
		else:
			if role11 in ctx.author.roles:
				await ctx.send(f'{ctx.author.mention}, ты сейчас выебан.')
			elif role33 in ctx.author.roles:
				if roles1 not in ctx.author.roles:
					await ctx.send(f'{ctx.author.mention}, ты сейчас не выебан, но был выебан ранее.')
			else:
				await ctx.send(f'{ctx.author.mention}, ты сейчас не выебан, и не был выебан ранее.')
	except MemberNotFound:
		await ctx.send(f'{ctx.author.mention}, пользователя нет на сервере.')

@client.command()
async def execc(ctx, *, command):
	if ctx.author.id in admins_id:
		"""Evaluate the given python code"""
		if match := re.fullmatch(r"(?:\n*)?`(?:``(?:py(?:thon)?\n)?((?:.|\n)*)``|(.*))`", command, re.DOTALL):
			code = match.group(1) if match.group(1) else match.group(2)
			str_obj = io.StringIO()  # Retrieves a stream of data
			try:
				with contextlib.redirect_stdout(str_obj):
					exec(code)
			except Exception as e:
				return await ctx.send(f"""❌ Your code completed with execution code 1
				```
				{e.__class__.__name__}: {e}
				```""")
			embed = discord.Embed(description="Error: Invalid format", color=0xED2525)
			return await ctx.send(embed=embed)
		return await ctx.send(f"""✅ Your code completed with execution code 0
				```
				{str_obj.getvalue()}
				```""")

	else:
		await ctx.send('а хуй тебе')

@client.command(aliases=['заскамить', 'скам'])
async def comand2(ctx, *, user: discord.Member=None):
	if user:
		if user.id not in admins_id:
			await ctx.send(f'{user.name}#{user.discriminator} ахаххахаха лох ипцчий заскамили мамонта лоха аахахах разрывная заскамленный хуедилдо азхахахахахахах хуй тимошин сосал лёжа на хуе розила ахахаааххахахахаххахахахахахаххахахахах')
		else:
			await ctx.send('ты не выёбывайся. админов скамить нельзя..')
		if user.id == client.user.id:
			await ctx.send('вот ты еблан, меня скамнуть не получится')
		else:
			pass
	else:
		await ctx.send('Пользователя пингани, которого скамнуть надо')

@client.command(aliases=['разьебать', 'разъебать'])
async def command333(ctx, *, user: discord.Member=None):
	if ctx.author.id in admins_id:
		server = discord.utils.get(client.guilds, id=server_id)
		role11 = discord.utils.get(server.roles, name='〘.!.〙Мать в канаве')
		role22 = discord.utils.get(server.roles, name='〘.!.〙Долбаеб')
		try:
			await user.remove_roles(role11)
			await user.remove_roles(role22)
			await ctx.send(f'{ctx.author.mention}, {user.mention} успешно разьёбан.')
		except:
			await ctx.send('чёт не вышло.')
	else:
		await ctx.send('пошёл ка нахуй, жди тимоху или самсунг ассистента.')

