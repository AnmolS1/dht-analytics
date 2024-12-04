from gui import run_gui
from print_to_file import print_to_file
from update_db import update_db
from appdirs import user_data_dir
import os, json

def setup():
	app_name: str = "HT-Metrics"
	app_author: str = "discoinferno"
	
	data_dir = user_data_dir(app_name, app_author)
	os.makedirs(data_dir, exist_ok=True)
	
	env_file = os.path.join(data_dir, "config.json")
	
	with open(env_file, 'r') as f:
		return json.load(f)

def main():
	config = setup()
	
	data = run_gui()
	
	if '' in data.values():
		return
	
	print_to_file(data, config['METRICS_SHEET_FILE_PATH'])
	update_db(data, config['POSTGRES_URL'])

if __name__ == '__main__':
	main()
