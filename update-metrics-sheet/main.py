from custom_types import Property
from dotenv import load_dotenv
from retrieve import retrieve
from print_to_file import print_to_file
import os

def setup() -> Property:
	load_dotenv()
	
	home_form_submit_info = (str(os.getenv('HOME_FORM_SUBMIT_ID')),)
	home_cta_info = (str(os.getenv('HOME_CTA_ID')), 'home_buy_now')
	mango_cta_info = (str(os.getenv('MANGO_CTA_ID')), 'mango_buy_now_click')
	rose_cta_info = (str(os.getenv('ROSE_CTA_ID')), 'rose buy now')
	
	return home_form_submit_info, home_cta_info, mango_cta_info, rose_cta_info

def main() -> None:
	yesterday, all_time = retrieve(setup())
	print_to_file(yesterday, all_time, str(os.getenv('METRICS_SHEET_FILE_PATH')))

if __name__ == '__main__':
	main()
