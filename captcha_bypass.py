from selenium import webdriver
from selenium.common.exceptions import TimeoutException as TE
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.common.by import By
import sys
from typing import Dict, Tuple
from time import sleep
from discord import Discord


class hCaptcha:
    def __init__(self, headers: Dict, webhook: str, email: str, password: str, count: int, webdriver: str = 'assets/chromedriver.exe', extension: str = 'assets/Tampermonkey.crx') -> None:
        self.webdriver_path = webdriver
        self.extension_path = extension
        self.headers = headers
        self.driver = self.webdriver()

        self.__email = email
        self.__password = password
        self.__count = count

        self.discord = Discord(webhook)
        self.discord.send(f"🎈 (#{self.__count}) Captcha bypass započat")

    def webdriver(self):
        options = webdriver.ChromeOptions()
        options.add_extension(self.extension_path)
        options.add_argument('--lang=en')
        # options.add_argument("--headless")  # Headless ChromeDriver.
        options.add_argument('log-level=3')
        options.add_argument('--mute-audio')
        options.add_argument("--enable-webgl-draft-extensions")
        options.add_argument("--ignore-gpu-blocklist")
        options.add_argument('--no-sandbox')

        for header in self.headers:
            options.add_argument(f"{header}=\"{self.headers[header]}\"")

        driver = webdriver.Chrome(self.webdriver_path, options=options)
        driver.maximize_window()

        return driver

    def element_clickable(self, element: str) -> None:
        WDW(self.driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, element))).click()

    def element_visible(self, element: str):
        return WDW(self.driver, 20).until(EC.visibility_of_element_located(
            (By.XPATH, element)))

    def window_handles(self, window_number: int) -> None:
        WDW(self.driver, 30).until(lambda _: len(
            self.driver.window_handles) == window_number + 1)
        self.driver.switch_to.window(self.driver.window_handles[window_number])

    def download_userscript(self) -> None:
        try:
            self.discord.send(f"🎈 (#{self.__count}) Zahájení instalace skriptu do prohlížeče")
            self.window_handles(1)
            self.driver.get('https://greasyfork.org/en/scripts/425854-hcaptcha'
                            '-solver-automatically-solves-hcaptcha-in-browser')
            self.element_clickable('//*[@id="install-area"]/a[1]')
            self.window_handles(2)
            self.element_clickable('//*[@value="Install"]')
            self.window_handles(1)
            self.driver.close()
            self.window_handles(0)
            self.discord.send(f":white_check_mark: (#{self.__count}) Script nainstalován do prohlížeče")
        except TE:
            self.discord.send(f"❌ (#{self.__count}) Chyba při stahování skriptu do prohlížeče")
            sys.exit('Failed')

    def freebitco(self, url: str) -> Tuple[bool, str]:
        try:
            self.discord.send(f"🎈 (#{self.__count}) Započato řešení captchy")
            self.driver.get(url)

            burger_menu = WDW(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu_drop"]/a')))
            burger_menu.click()

            login = WDW(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/nav/section/ul/li[10]/a')))
            login.click()

            email = WDW(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_form_btc_address"]')))
            password = WDW(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_form_password"]')))
            login_button = self.driver.find_element_by_xpath('//*[@id="login_button"]')

            email.send_keys(self.__email)
            password.send_keys(self.__password)

            self.driver.execute_script("arguments[0].click();", login_button)

            WDW(self.driver, 800).until(lambda _: len(self.element_visible(
                '//div[@class="h-captcha"]/iframe').get_attribute(
                    'data-hcaptcha-response')) > 0)

            roll_button = self.driver.find_element_by_xpath('//*[@id="free_play_form_button"]')
            self.driver.execute_script("arguments[0].click();", roll_button)

            sleep(10)

            balance = self.driver.find_element_by_xpath('//*[@id="balance"]').text
            if not balance:
                balance = self.driver.find_element_by_xpath('//*[@id="balance_small"]').text

            sleep(1.5)

            self.driver.quit()

            return (True, balance)
        except TE:
            self.driver.quit()

            return (False, "unknown")