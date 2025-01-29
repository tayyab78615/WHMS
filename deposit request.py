import time
import logging
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

# Configure logging
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

    def select_autocomplete_option(self, label_text, option_text):
        """Select an option from the Material-UI Autocomplete dropdown by label."""
        try:
            input_locator = f"//label[contains(text(), '{label_text}')]/following-sibling::div//input"
            input_field = self.wait.until(EC.element_to_be_clickable((By.XPATH, input_locator)))
            input_field.click()
            logger.info(f"Clicked on input field with label '{label_text}'")

            time.sleep(2)

            option_locator = f"//li[contains(text(), '{option_text}')]"
            option_element = self.wait.until(EC.presence_of_element_located((By.XPATH, option_locator)))
            logger.info(f"Dropdown option locator: {option_locator}")

            option_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_locator)))
            option_element.click()
            logger.info(f"Selected option '{option_text}' from dropdown")
        except Exception as e:
            logger.error(f"Error selecting option from Autocomplete dropdown '{label_text}' with option '{option_text}': {e}")

    def run(self):
        """Run the complete automation process."""
        try:
            self.driver.get(self.url)
            self.fill_field('email', 'vako@mailinator.com')
            self.fill_field('auth-login-v2-password', 'Test@1234')
            self.click_element('login-button', By.ID)

            self.search_and_click('Deposit Request')
            self.search_and_click('Add New')

            logger.info("Waiting for the page to load...")
            time.sleep(random.uniform(3, 6))

            self.select_autocomplete_option('Select Warehouse', 'Karachi Central Warehouse')
            time.sleep(2)
            self.select_autocomplete_option('Select Vendor', 'Hyatt Cardenas ')
            
            # Fill description field
            self.fill_field('description', 'Your description text here')
            
            # Click Generate DRN button
            self.click_element('create', By.ID)

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