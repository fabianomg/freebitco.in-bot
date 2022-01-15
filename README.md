# Freebitco.in BOT
## Disclaimer
I'm not responsible for you and your account on *freebitco.in* site. This script is against *freebitco.in* ToS and you **may get banned**.

## Requirements
* This script works only on devices with display, e.g. Ubuntu Desktop, Windows, ...
* Chromedriver

## Installation - Ubuntu Desktop 20.04
* Install packgaes

```
sudo apt install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget chromium-browser chromium-chromedriver python3-pip build-essential libssl-dev libffi-dev python3-dev python3-venv openssh-client git
```

* Clone github repo

```
git clone git@github.com:Javierko/freebitco.in-bot.git
```

* Install python requirements

```
pip install -r requirements.txt
```

* Create .env and fill the data

```
cp .env.example .env
```

## Enviroment

* `EMAIL` - your email to *freebitco.in* app
* `PASSWORD` - password to your *freebitco.in* app
* `WEBHOOK` - Webhook for Discord to send log messages
* `URL` - should be `https://freebitco.in/?op=home#`
* `FILE` - file to store the value of "round", should be just `counter.txt`
* `WEBDRIVER` - path to chrome web driver, on Ubuntu should be `/usr/bin/chromedriver`
* `EXTENSION` - path to `Tampermonkey.crx` extension, e.g. `/home/test/freebitco.in-bot/assets/Tampermonkey.crx`
* `PRIVACYPASS` - path to `PrivacyPass.crx` extension, e.g. `/home/test/freebitco.in-bot/assets/PrivacyPass.crx`

## Credits
* [maximedrn's hcaptcha solver](https://github.com/maximedrn/hcaptcha-solver-python-selenium)
