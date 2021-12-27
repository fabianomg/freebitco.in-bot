from captcha_bypass import hCaptcha
from discord import Discord
from dotenv import load_dotenv
import os
import sched
import time
import subprocess


load_dotenv()


def do_something(sc, hcaptcha, count, discord):
    count += 1

    finished, balance = hcaptcha.freebitco(os.getenv("URL"))

    if finished:
        discord.send(
            f":white_check_mark: (#{count}) Získávání dokončeno - {balance} BTC")
    else:
        discord.send(f"❌ (#{count}) Ukončeno - nedošlo k získání bitcoinů")

    with open(os.getenv("FILE"), "w") as file:
        file.write(str(count))

    s.enter(1200, 1, do_something, (sc, hcaptcha, count, discord))


if __name__ == "__main__":
    s = sched.scheduler(time.time, time.sleep)

    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    for line in out.splitlines():
        line = line.decode()

        if not 'chrome' in line:
            continue

        pid = int(line.split(None, 1)[0])
        os.kill(pid, -9)

    count: int = 1

    if os.path.exists(os.getenv("FILE")):
        with open("counter.txt") as file:
            count = int(file.readline())

    discord = Discord(os.getenv("WEBHOOK"))
    discord.send(f"🎈 (#{count}) Bitcoin BOT zapnut")

    hcaptcha = hCaptcha(os.getenv("WEBHOOK"), os.getenv("EMAIL"), os.getenv(
        "PASSWORD"), count, os.getenv("WEBDRIVER"), [os.getenv("EXTENSION"), os.getenv("PRIVACYPASS")])
    hcaptcha.download_userscript()

    s.enter(5, 1, do_something, (s, hcaptcha, count, discord))
    s.run()
