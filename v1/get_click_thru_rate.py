from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import sys
import os

driver, wait = None, None
ig_username, ig_password = None, None

def setup():
	chrome_options = Options()
	chrome_options.add_experimental_option(
		"prefs", {
			"profile.default_content_setting_values.notifications": 2
		}
	)
	chrome_options.add_argument("--headless=new")
	
	service = Service('./chromedriver')
	
	load_dotenv()
	global driver, wait, ig_username, ig_password
	
	driver = webdriver.Chrome(service=service, options=chrome_options)
	wait = WebDriverWait(driver, 10)
	
	ig_username = os.getenv('IG_USERNAME')
	ig_password = os.getenv('IG_PASSWORD')

def login():
	if not driver or not wait:
		print('Driver failed to initialize')
		sys.exit(1)
	
	driver.get('https://business.facebook.com/')
	
	original_window_handle = driver.current_window_handle
	
	login_with_ig_btn = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role=\'button\']')))[1]
	login_with_ig_btn.click()
	
	try:
		wait.until(EC.number_of_windows_to_be(2))
		for handle in driver.window_handles:
			if handle != original_window_handle:
				driver.switch_to.window(handle)
				break
	except:
		original_window_handle = None
	
	username_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name=\'username\']')))
	password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name=\'password\']')))
	username_input.send_keys(str(ig_username))
	password_input.send_keys(str(ig_password))
	
	login_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type=\'submit\']')))
	login_btn.click()
	
	save_login_info_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//div[text()=\'Not now\']')))
	save_login_info_btn.click()
	
	if original_window_handle:
		wait.until(EC.number_of_windows_to_be(1))
		driver.switch_to.window(original_window_handle)

def get_reach() -> int:
	if not driver or not wait:
		print('Driver failed to initialize')
		sys.exit(1)
	
	driver.get('https://business.facebook.com/latest/insights/overview/?business_id=561788986340298&asset_id=471205406070851')
	
	view_all_insights_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//div[text()=\'View all insights\']')))
	view_all_insights_btn.click()
	
	reach = wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()=\'Total\']/../../../div[last()]/div')))
	return int(reach.text.replace(',', ''))

def get_click_thru_rate(website_visits: int) -> str:
	try:
		setup()
		login()
		reach = get_reach()
	finally:
		if not driver:
			print('Chromedriver did not initialize, you def fucked up something bc this script is flawless so fuck you')
			sys.exit(1)
		
		driver.quit()
	
	click_thru_rate = website_visits / reach * 100
	
	return f'{click_thru_rate:.2f}'

if __name__ == '__main__':
	from get_conversion_rate import get_website_visits_only
	print(f'current click through rate: {get_click_thru_rate(get_website_visits_only())}%')
