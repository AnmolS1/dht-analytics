from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta
import urllib.parse
import os, sys

driver, wait = None, None
ig_user, ig_pass = None, None

def setup():
	options = Options()
	options.add_experimental_option(
		'prefs', {
			'profile.default_content_setting_values.notifications': 2
		}
	)
	options.add_argument('--headless=new')
	
	service = Service('./chromedriver')
	
	global driver, wait, ig_user, ig_pass
	
	driver = webdriver.Chrome(service=service, options=options)
	wait = WebDriverWait(driver, 10)
	
	ig_user = os.getenv('IG_USERNAME')
	ig_pass = os.getenv('IG_PASSWORD')

def meta_login():
	if not driver or not wait:
		print(f'Driver failed to initialize')
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
	username_input.send_keys(str(ig_user))
	password_input.send_keys(str(ig_pass))
	
	login_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type=\'submit\']')))
	login_btn.click()
	
	save_login_info_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//div[text()=\'Not now\']')))
	save_login_info_btn.click()
	
	if original_window_handle:
		wait.until(EC.number_of_windows_to_be(1))
		driver.switch_to.window(original_window_handle)

def get_reach() -> tuple[int, int]:
	if not driver or not wait:
		print(f'Driver failed to initialize')
		sys.exit(1)
	
	yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
	total_range = urllib.parse.quote(urllib.parse.quote('{"end":"' + yesterday + '","start":"2024-10-19"}', safe=''), safe='')
	yesterday_range = urllib.parse.quote(urllib.parse.quote('{"end":"' + yesterday + '","start":"' + yesterday + '"}', safe=''), safe='')
	
	driver.get(f'https://business.facebook.com/latest/insights/overview/?business_id=561788986340298&asset_id=471205406070851&time_range={total_range}')
	
	view_all_insights_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//div[text()=\'View all insights\']')))
	view_all_insights_btn.click()
	
	total_reach = wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()=\'Total\']/../../../div[last()]/div'))).text
	
	driver.get(f'https://business.facebook.com/latest/insights/overview/?business_id=561788986340298&asset_id=471205406070851&time_range={yesterday_range}')
	
	yesterday_reach = wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()=\'Total\']/../../../div[last()]/div'))).text
	
	return int(total_reach.replace(',', '')), int(yesterday_reach.replace(',', ''))

def get_views() -> int:
	if not driver or not wait:
		print(f'Driver failed to initialize')
		sys.exit(1)
	
	driver.get('https://www.instagram.com/accounts/insights/?timeframe=30')
	total_views = wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()=\'Views\']/../../../../div[last()]/div/div/div/span'))).text
	
	return int(total_views.replace(',', ''))

def get_data_points() -> tuple[int, int, int]:
	setup()
	
	meta_login()
	all_time_reach, yesterday_reach = get_reach()
	
	all_time_views = get_views()
	
	return all_time_reach, yesterday_reach, all_time_views
