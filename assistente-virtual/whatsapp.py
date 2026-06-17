import os
import shutil
import time
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def find_browser(browser_name: str) -> Optional[str]:
    candidates = []
    if browser_name == "chrome":
        candidates = ["google-chrome", "chrome", "chromium-browser", "chromium"]
    elif browser_name == "firefox":
        candidates = ["firefox"]

    for candidate in candidates:
        path = shutil.which(candidate)
        if path:
            return path
    return None


class WhatsAppConnector:
    """Conecta ao WhatsApp Web usando Selenium."""

    def __init__(self, profile_dir: Optional[str] = None, headless: bool = False, browser: str = "chrome"):
        self.profile_dir = profile_dir or os.path.join(os.getcwd(), ".whatsapp-profile")
        self.headless = headless
        self.browser = browser.lower()
        self.driver = None

    def _build_chrome(self):
        chrome_path = find_browser("chrome")
        if not chrome_path:
            raise RuntimeError("Chrome/Chromium não encontrado no sistema.")

        options = ChromeOptions()
        options.binary_location = chrome_path
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument(f"--user-data-dir={self.profile_dir}")
        if self.headless:
            options.add_argument("--headless=new")

        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _build_firefox(self):
        firefox_path = find_browser("firefox")
        if not firefox_path:
            raise RuntimeError("Firefox não encontrado no sistema.")

        options = FirefoxOptions()
        options.binary_location = firefox_path
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if self.headless:
            options.add_argument("-headless")

        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    def connect(self, timeout: int = 120):
        if self.browser == "firefox":
            self.driver = self._build_firefox()
        else:
            self.driver = self._build_chrome()

        self.driver.get("https://web.whatsapp.com")
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="3"], div[contenteditable="true"][data-tab="4"]')
                )
            )
        except TimeoutException as exc:
            raise RuntimeError("Tempo esgotado ao carregar WhatsApp Web. Certifique-se de escanear o QR Code.") from exc

        print("Conectado ao WhatsApp Web com sucesso.")
        return self

    def _find_search_box(self):
        selectors = [
            'div[contenteditable="true"][data-tab="3"]',
            'div[contenteditable="true"][data-tab="4"]',
        ]
        for selector in selectors:
            try:
                return self.driver.find_element(By.CSS_SELECTOR, selector)
            except NoSuchElementException:
                continue
        raise RuntimeError("Campo de busca do WhatsApp não encontrado.")

    def _find_message_box(self):
        selectors = [
            'div[contenteditable="true"][data-tab="10"]',
            'div[contenteditable="true"][data-tab="9"]',
        ]
        for selector in selectors:
            try:
                return self.driver.find_element(By.CSS_SELECTOR, selector)
            except NoSuchElementException:
                continue
        raise RuntimeError("Campo de mensagem do WhatsApp não encontrado.")

    def send_message(self, contact: str, message: str):
        if self.driver is None:
            raise RuntimeError("Conexão não estabelecida. Chame connect() antes de enviar mensagens.")

        search_box = self._find_search_box()
        search_box.click()
        search_box.clear()
        search_box.send_keys(contact)
        search_box.send_keys("\n")
        time.sleep(2)

        message_box = self._find_message_box()
        message_box.click()
        message_box.send_keys(message)
        message_box.send_keys("\n")

        print(f"Mensagem enviada para {contact}.")

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None


if __name__ == "__main__":
    connector = WhatsAppConnector(headless=False, browser="chrome")
    try:
        connector.connect()
        print("WhatsApp Web aberto. Escaneie o QR Code se necessário.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Encerrando a conexão do WhatsApp.")
    except Exception as exc:
        print("Erro:", exc)
    finally:
        connector.close()
import os
import shutil
import sys
import time
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def find_browser(browser_name: str) -> Optional[str]:
    candidates = []
    if browser_name == "chrome":
        candidates = ["google-chrome", "chrome", "chromium-browser", "chromium"]
    elif browser_name == "firefox":
        candidates = ["firefox"]

    for candidate in candidates:
        path = shutil.which(candidate)
        if path:
            return path
    return None


class WhatsAppConnector:
    """Conecta ao WhatsApp Web usando Selenium."""

    def __init__(self, profile_dir: Optional[str] = None, headless: bool = False, browser: str = "chrome"):
        self.profile_dir = profile_dir or os.path.join(os.getcwd(), ".whatsapp-profile")
        self.headless = headless
        self.browser = browser.lower()
        self.driver = None

    def _build_chrome(self):
        chrome_path = find_browser("chrome")
        if not chrome_path:
            raise RuntimeError("Chrome/Chromium não encontrado no sistema.")

        options = ChromeOptions()
        options.binary_location = chrome_path
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--user-data-dir=%s" % self.profile_dir)
        if self.headless:
            options.add_argument("--headless=new")

        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _build_firefox(self):
        firefox_path = find_browser("firefox")
        if not firefox_path:
            raise RuntimeError("Firefox não encontrado no sistema.")

        options = FirefoxOptions()
        options.binary_location = firefox_path
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if self.headless:
            options.add_argument("-headless")

        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    def connect(self, timeout: int = 120):
        if self.browser == "firefox":
            self.driver = self._build_firefox()
        else:
            self.driver = self._build_chrome()

        self.driver.get("https://web.whatsapp.com")
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="3"], div[contenteditable="true"][data-tab="4"]')
                )
            )

            print("Conectado ao WhatsApp Web com sucesso.")
            return self
        except TimeoutException:
            print("Tempo esgotado aguardando o carregamento do WhatsApp Web.")
        return None
        
        
        def _find_search_box(self):
            selectors = [
                'div[contenteditable="true"][data-tab="3"]',
                'div[contenteditable="true"][data-tab="4"]',
            ]
            for selector in selectors:
                try:
                    return self.driver.find_element(By.CSS_SELECTOR, selector)
                except NoSuchElementException:
                    continue
            raise RuntimeError("Campo de busca do WhatsApp não encontrado.")

        def _find_message_box(self):
            selectors = [
                'div[contenteditable="true"][data-tab="10"]',
                'div[contenteditable="true"][data-tab="9"]',
            ]
            for selector in selectors:
                try:
                    return self.driver.find_element(By.CSS_SELECTOR, selector)
                except NoSuchElementException:
                    continue
            raise RuntimeError("Campo de mensagem do WhatsApp não encontrado.")

        def send_message(self, contact: str, message: str):
            if self.driver is None:
                raise RuntimeError("Conexão não estabelecida. Chame connect() antes de enviar mensagens.")

            search_box = self._find_search_box()
            search_box.click()
            search_box.clear()
            search_box.send_keys(contact)
            search_box.send_keys("\n")
            time.sleep(2)

            message_box = self._find_message_box()
            message_box.click()
            message_box.send_keys(message)
            message_box.send_keys("\n")

            print(f"Mensagem enviada para {contact}.")

        def close(self):
            if self.driver:
                self.driver.quit()
                self.driver = None


    if __name__ == "__main__":
        connector = WhatsAppConnector(headless=False, browser="chrome")
        try:
            connector.connect()
            print("WhatsApp Web aberto. Escaneie o QR Code se necessário.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Encerrando a conexão do WhatsApp.")
        except Exception as exc:
            print("Erro:", exc)
        finally:
            connector.close()
