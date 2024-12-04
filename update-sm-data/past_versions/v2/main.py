from argparse import ArgumentParser, Namespace
from dotenv import load_dotenv
import psycopg, json, os

yesterdays_reach, yesterdays_views, all_time_reach, all_time_views = None, None, None, None

def setup() -> None:
	def get_args() -> Namespace:
		parser = ArgumentParser()
		
		parser.add_argument('--yesterday-reach', '-yr', type=int, required=True)
		parser.add_argument('--all-time-reach', '-ar', type=int, required=True)
		parser.add_argument('--yesterday-views', '-yv', type=int, required=True)
		parser.add_argument('--all-time-views', '-av', type=int, required=True)
		
		return parser.parse_args()
	
	load_dotenv()
	args = get_args()
	
	global yesterdays_reach, yesterdays_views, all_time_reach, all_time_views
	
	yesterdays_reach = args.yesterday_reach
	yesterdays_views = args.yesterday_views
	all_time_reach = args.all_time_reach
	all_time_views = args.all_time_views

def update_db() -> None:
	curr_metrics = {}
	
	with psycopg.connect(str(os.getenv('POSTGRES_URL'))) as conn:
		with conn.cursor() as cursor:
			cursor.execute('SELECT * FROM metrics_db WHERE type != \'Last 30 Minutes\'')
			
			for row in cursor.fetchall():
				curr_metrics[row[0]] = json.loads(row[1])
	
	curr_metrics['Yesterday']['data_points']['reach'] = yesterdays_reach
	curr_metrics['Yesterday']['data_points']['views'] = yesterdays_views
	
	curr_metrics['All Time']['data_points']['reach'] = all_time_reach
	curr_metrics['All Time']['data_points']['views'] = all_time_views
	
	curr_metrics['Yesterday']['metrics']['uctr'] = round((curr_metrics['Yesterday']['data_points']['visitors'] / curr_metrics['Yesterday']['data_points']['reach']) * 100)
	curr_metrics['Yesterday']['metrics']['gctr'] = round((curr_metrics['Yesterday']['metrics']['visits'] / curr_metrics['Yesterday']['data_points']['views']) * 100)
	
	curr_metrics['All Time']['metrics']['uctr'] = round((curr_metrics['All Time']['data_points']['visitors'] / curr_metrics['All Time']['data_points']['reach']) * 100)
	curr_metrics['All Time']['metrics']['gctr'] = round((curr_metrics['All Time']['metrics']['visits'] / curr_metrics['All Time']['data_points']['views']) * 100)
	
	with psycopg.connect(str(os.getenv('POSTGRES_URL'))) as conn:
		with conn.cursor() as cursor:
			query = "UPDATE metrics_db SET data = %s::jsonb WHERE type = %s"
			
			cursor.execute(query, (json.dumps(curr_metrics["Yesterday"]), 'Yesterday'))
			cursor.execute(query, (json.dumps(curr_metrics["All Time"]), 'All Time'))
			
			conn.commit()

def main() -> None:
	setup()
	update_db()

if __name__ == '__main__':
	main()
