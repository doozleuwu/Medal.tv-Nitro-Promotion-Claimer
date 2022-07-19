import requests, random, string, os, ctypes
from itertools import product, cycle
from threading import Thread

class medal():
    def __init__(self):
        self.banner = """
                                                              \x1b[38;5;63m╔═╗╔╗╔╔═╗╦ ╦
                                                              \x1b[38;5;63m╚═╗║║║║ ║║║║
                                                              \x1b[38;5;63m╚═╝╝╚╝╚═╝╚╩╝
                                                            \u001b[0mdoozle \x1b[\x1b[38;5;63mX \x1b[0mdiscord"""
        print(self.banner)
        with open("data/proxies.txt", encoding="utf-8") as f:
            self.proxies = [i.strip() for i in f]
        self.proxy_pool = cycle(self.proxies)
        with open("data/tokens.txt", encoding="utf-8") as f:
            self.tokens = [i.strip() for i in f]
        self.tokens_pool = cycle(self.tokens)
        self.threads = int(input('\u001b[0m[\x1b[\x1b[38;5;63m/\u001b[0m] Threads \x1b[\x1b[38;5;63m>> \u001b[0m'))
        print('\u001b[0m[\x1b[\x1b[38;5;63m/\u001b[0m] Starting %s thread(s)...\n' % self.threads)
        self.acccounter = 0
        self.promocounter = 0
        self.beginMain()

    def title(self):
        ctypes.windll.kernel32.SetConsoleTitleW("[snow] Threads (%s) | Created (%s) | Promotions (%s/%s)" % (self.threads, self.acccounter, self.promocounter, self.acccounter))

    def createEmail(self):
        randomEmail = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(12))
        return f'{randomEmail}@guilded.lol'

    def randomString(self):
        randomString = ''.join(random.choice(string.ascii_lowercase) for i in range(15))
        return randomString
    
    def registerMedal(self):
        try:
            email = self.createEmail()
            password = self.randomString()
            reg = {'email': email, 'userName': password, 'password': password}
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'User-Agent': 'Medal-Electron/4.1674.0 (string_id_v2; no_upscale) win32/10.0.19042 (x64) Electron/8.5.5 Recorder/1.0.0 Node/12.13.0 Chrome/80.0.3987.163 Environment/production',  'Medal-User-Agent': 'Medal-Electron/4.1674.0 (string_id_v2; no_upscale) win32/10.0.19042 (x64) Electron/8.5.5 Recorder/1.0.0 Node/12.13.0 Chrome/80.0.3987.163 Environment/production'}
            r = requests.post("https://medal.tv/api/users", json=reg, headers=headers, proxies={"https": f"http://{next(self.proxy_pool)}"})
            if r.status_code == 200:
                auth = {'email': email, 'password': password}
                r = requests.post("https://medal.tv/api/authentication", json=auth, headers=headers, proxies={"https": f"http://{next(self.proxy_pool)}"}).json()
                token = r['userId'] + ',' + r['key']
                userID = r['userId']
                key = r['key']
                print('\u001b[0m[\x1b[\x1b[38;5;63m$\u001b[0m] %s \u001b[0m' % 'Successfully registered medal.tv account!')
                self.acccounter += 1
                self.title()
                return token, userID, key
        except Exception:
            print('\u001b[0m[\x1b[\x1b[38;5;63m#\u001b[0m] %s \u001b[0m' % 'Failed to register medal.tv account, trying again!')
            self.registerMedal()
    
    def discordOauth(self):
        try:
            token = self.registerMedal()[0]
            discordToken = next(self.tokens_pool)
            r = requests.post('https://medal.tv/social-api/connections', json={'provider': 'discord'}, headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'User-Agent': 'Medal-Electron/4.1674.0 (string_id_v2; no_upscale) win32/10.0.19042 (x64) Electron/8.5.5 Recorder/1.0.0 Node/12.13.0 Chrome/80.0.3987.163 Environment/production',  'Medal-User-Agent': 'Medal-Electron/4.1674.0 (string_id_v2; no_upscale) win32/10.0.19042 (x64) Electron/8.5.5 Recorder/1.0.0 Node/12.13.0 Chrome/80.0.3987.163 Environment/production', 'X-Authentication': token}, proxies={"https": f"http://{next(self.proxy_pool)}"}).json()
            x = requests.post(r['loginUrl'], headers={'Authorization': discordToken, 'Content-Type': 'application/json'}, json={'permissions':'0', 'authorize':'true'}, proxies={"https": f"http://{next(self.proxy_pool)}"}).json()
            requests.get(x['location'])
            nitroLink = requests.get('https://medal.tv/api/social/discord/nitroCode', headers={'Accept':'application/json', 'Content-Type':'application/json', 'User-Agent': 'Medal-Electron/4.1674.0 (string_id_v2; no_upscale) win32/10.0.19042 (x64) Electron/8.5.5 Recorder/1.0.0 Node/12.13.0 Chrome/80.0.3987.163 Environment/production', 'Medal-User-Agent': 'Medal-Electron/4.1674.0 (string_id_v2; no_upscale) win32/10.0.19042 (x64) Electron/8.5.5 Recorder/1.0.0 Node/12.13.0 Chrome/80.0.3987.163 Environment/production', 'X-Authentication': token}, proxies={"https": f"http://{next(self.proxy_pool)}"}).json() 
            print('\u001b[0m[\x1b[\x1b[38;5;63m$\u001b[0m] %s \u001b[0m' % nitroLink['url'])
            with open("results/promos.txt", "a+") as f: f.write('%s\n' % nitroLink['url'])
            self.promocounter += 1
            self.title()
        except Exception as e:
            print('\u001b[0m[\x1b[\x1b[38;5;63m#\u001b[0m] %s \u001b[0m' % f'{discordToken} is ineligible to claim promotion!')
            pass

    def beginMain(self):
        for x in range(self.threads):
            Thread(target=self.discordOauth).start()

if __name__ == '__main__':
    os.system("cls & mode 140,24")
    doozle = medal()
