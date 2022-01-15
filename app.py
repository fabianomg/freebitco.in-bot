from captcha_bypass import hCaptcha
from discord import Discord
from dotenv import load_dotenv
import os
import subprocess
import platform

def isLinux() -> bool:
    return platform.system().lower().startswith('lin')

if isLinux():
    from signal import SIGKILL

load_dotenv()


if __name__ == "__main__":
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    for line in out.splitlines():
        line = line.decode()

        if not 'chrome' in line:
            continue

        pid = int(line.split(None, 1)[0])
        os.kill(pid, SIGKILL if isLinux() else -9)

    count: int = 1

    if os.path.exists(os.getenv("FILE")):
        with open("counter.txt") as file:
            count = int(file.readline())

    discord = Discord(os.getenv("WEBHOOK"))
    discord.send(f"🎈 (#{count}) Bitcoin BOT zapnut")

    hcaptcha = hCaptcha(os.getenv("WEBHOOK"), os.getenv("EMAIL"), os.getenv(
        "PASSWORD"), count, os.getenv("WEBDRIVER"), [os.getenv("EXTENSION"), os.getenv("PRIVACYPASS")])
    hcaptcha.download_userscript()

    count += 1

    finished, balance = hcaptcha.freebitco(os.getenv("URL"))

    if finished:
        discord.send(f":white_check_mark: (#{count}) Program finished - {balance} BTC")
    else:
        discord.send(f"❌ (#{count}) Program failed")

    with open(os.getenv("FILE"), "w") as file:
        file.write(str(count))
