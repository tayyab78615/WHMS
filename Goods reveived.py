import time
import logging
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FormAutomation:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 40)
        self.url = url

    def fill_field(self, locator, value, by=By.ID):
        """Fill a text field with a given value."""
        try:
            element = self.wait.until(EC.presence_of_element_located((by, locator)))
            element.clear()
            element.send_keys(value)
            logger.info(f"Filled field '{locator}' with value '{value}'")
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Error filling field '{locator}': {e}")

    def click_element(self, locator, by=By.XPATH):
        """Click an element located by XPath or ID."""
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, locator)))
            element.click()
            logger.info(f"Clicked element '{locator}'")
        except (TimeoutException, ElementClickInterceptedException) as e:
            logger.error(f"Error clicking element '{locator}': {e}")

    def search_and_click(self, text):
        """Search for an element by its visible text and click it."""
        try:
            locator = f"//*[contains(text(), '{text}')]"
            self.click_element(locator, By.XPATH)
            logger.info(f"Clicked on text '{text}'")
        except Exception as e:
            logger.error(f"Error searching and clicking '{text}': {e}")

    def run(self):
        """Run the complete automation process."""
        try:
            self.driver.get(self.url)
            self.fill_field('email', 'vako@mailinator.com')
            self.fill_field('auth-login-v2-password', 'Test@1234')
            self.click_element('login-button', By.ID)

            self.search_and_click('Goods Received')

            time.sleep(2)

            self.search_and_click('Create GRN')

            time .sleep(2)

            self.fill_field('drnNumber', '000720250128DRN')

            time.sleep(2)

            self.search_and_click('Fetch DRN Details')

            logger.info("Waiting for the page to load...")
            time.sleep(random.uniform(3, 6))

        except Exception as e:
            logger.error(f"Error in automation: {e}")
        finally:
            logger.info("Pausing before closing browser...")
            time.sleep(random.uniform(8, 12))
            logger.info("Closing browser...")
            self.driver.quit()


if __name__ == "__main__":
    automation = FormAutomation("http://localhost:3000")
    automation.run()