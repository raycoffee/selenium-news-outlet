import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from browserstack.local import Local
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
import time
from concurrent.futures import ThreadPoolExecutor
import logging
from config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_credentials():
   if not BROWSERSTACK_USERNAME or not BROWSERSTACK_ACCESS_KEY:
       raise ValueError("BrowserStack credentials not found")

def create_driver_options(config):
   
   options = webdriver.ChromeOptions()  # Default to Chrome options
   
   bstack_options = {
       'userName': BROWSERSTACK_USERNAME,
       'accessKey': BROWSERSTACK_ACCESS_KEY,
       'buildName': 'El Pais Scraper Build',
       'sessionName': config.get('name'),
       'debug': True,
       'networkLogs': True
   }
   
   # For desktop browsers
   if 'os' in config:
       bstack_options.update({
           'os': config['os'],
           'osVersion': config['os_version'],
           'browserVersion': config['browser_version']
       })
       
       if config['browser'] == 'Safari':
           options = webdriver.SafariOptions()
       elif config['browser'] == 'Firefox':
           options = webdriver.FirefoxOptions()
   
   # For mobile devices
   if 'device' in config:
       bstack_options.update({
           'deviceName': config['device'],
           'osVersion': config['os_version'],
           'realMobile': 'true'
       })
       if 'iPhone' in config['device']:
           options = webdriver.SafariOptions()
       else:
           options = webdriver.ChromeOptions()
   
   bstack_options = {k: v for k, v in bstack_options.items() if v is not None}
   
   options.set_capability('bstack:options', bstack_options)
   return options

def get_browser_config():
   return [
       # Desktop Browsers
       {
           'browser': 'Chrome',
           'os': 'Windows',
           'os_version': '11',
           'browser_version': 'latest',
           'name': 'El Pais Scraper - Windows Chrome'
       },
       {
           'browser': 'Firefox',
           'os': 'Windows',
           'os_version': '11',
           'browser_version': 'latest',
           'name': 'El Pais Scraper - Windows Firefox'
       },
       {
           'browser': 'Safari',
           'os': 'OS X',
           'os_version': 'Sonoma',
           'browser_version': 'latest',
           'name': 'El Pais Scraper - Mac Safari'
       },
       
       # Mobile Browsers
       {
           'device': 'iPhone 14',
           'os_version': '16',
           'name': 'El Pais Scraper - iPhone'
       },
       {
           'device': 'Samsung Galaxy S23',
           'os_version': '13.0',
           'name': 'El Pais Scraper - Android'
       }
   ]

def run_session(config):
   logger.info(f"Starting session for {config['name']}")
   try:
       logger.info("Connecting to BrowserStack...")
       options = create_driver_options(config)
       driver = webdriver.Remote(
           command_executor=f'https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub',
           options=options
       )
       
       build_url = f"https://automate.browserstack.com/builds/{driver.session_id}"
       logger.info(f"BrowserStack Build Link: {build_url}")
       
       logger.info("Navigating to El Pais...")
       driver.get("https://elpais.com/opinion/")
       
       wait = WebDriverWait(driver, 20)
       logger.info("Looking for articles...")
       articles_elements = wait.until(
           EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article"))
       )[:5]
       
       articles_data = []
       for idx, article_element in enumerate(articles_elements, 1):
           logger.info(f"Processing article {idx}/5...")
           title_text, content_text = "", ""
           
           try:
               title_element = article_element.find_element(By.CSS_SELECTOR, "h2 a")
               title_text = driver.execute_script(
                   "return arguments[0].textContent.trim()",
                   title_element
               )
               logger.info(f"Found title: {title_text[:50]}...")
           except Exception as e:
               logger.error(f"Title error: {e}")
               
           try:
               content_element = article_element.find_element(By.CSS_SELECTOR, "p")
               content_text = driver.execute_script(
                   "return arguments[0].textContent.trim()",
                   content_element
               )
               logger.info(f"Found content: {content_text[:50]}...")
           except Exception as e:
               logger.error(f"Content error: {e}")
               
           articles_data.append({
               "title": title_text,
               "content": content_text
           })
           
       logger.info(f"Successfully scraped {len(articles_data)} articles")
       driver.execute_script(
           'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Articles successfully scraped!"}}'
       )
       
   except Exception as e:
       logger.error(f"Test failed: {str(e)}")
       if 'driver' in locals():
           try:
               driver.execute_script(
                   'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Test failed"}}'
               )
           except:
               pass
   
   finally:
       if 'driver' in locals():
           logger.info("Closing browser session...")
           try:
               driver.quit()
           except:
               pass

if __name__ == '__main__':
   validate_credentials()
   logger.info("Starting BrowserStack tests...")
   configs = get_browser_config()
   
   logger.info(f"Running tests on {len(configs)} platforms:")
   for idx, config in enumerate(configs, 1):
       logger.info(f"{idx}. {config['name']}")
   
   with ThreadPoolExecutor(max_workers=5) as executor: 
       try:
           executor.map(run_session, configs)
       except Exception as e:
           logger.error(f"Error in test execution: {e}")
   
   logger.info("All tests completed!")