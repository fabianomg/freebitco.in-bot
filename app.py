from requests_html import HTMLSession
from bs4 import BeautifulSoup
from captcha_bypass import hCaptcha
from discord import Discord
from dotenv import load_dotenv
import os


load_dotenv()


if __name__ == "__main__":
    count: int = 1

    if os.path.exists(os.getenv("FILE")):
        with open("counter.txt") as file:
            count = int(file.readline())

    discord = Discord(os.getenv("WEBHOOK"))
    discord.send(f"🎈 (#{count}) Bitcoin BOT zapnut")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'Cookie': os.getenv("COOKIE"),
        'x-csrf-token': os.getenv("CSRF")
    }

    session = HTMLSession(headers=headers)

    response = session.get(os.getenv("URL"))
    response.html.render(timeout=20)

    soup = BeautifulSoup(response.html.html, "html.parser")
    time_remaining = soup.find("div", id = "time_remaining").find_all("span", class_ = "countdown_amount")

    if len(time_remaining) > 0:
        discord.send(f"❌ (#{count}) Bitcoin BOT ukončen, čas pro nový roll: {time_remaining[0].text}:{time_remaining[1].text}")
    else:
        hcaptcha = hCaptcha(headers, os.getenv("WEBHOOK"), os.getenv("EMAIL"), os.getenv("PASSWORD"), count, os.getenv("WEBDRIVER"), os.getenv("EXTENSION"))
        hcaptcha.download_userscript()
        finished, balance = hcaptcha.freebitco(os.getenv("URL"))

        if finished:
            discord.send(f":white_check_mark: (#{count}) Úspěšně získány bitcoiny - {balance} BTC")
        else:
            discord.send(f"❌ (#{count}) Chyba při získávání bitcoinů")
        
        count += 1

        with open(os.getenv("FILE"), "w") as file:
            file.write(str(count))

    