from dotenv import load_dotenv
from get_data_points import get_data_points
import psycopg
import os
import json

def update_db(all_time_reach: int, yesterday_reach: int, all_time_views: int) -> None:
	curr_metrics = {}
	
	with psycopg.connect(str(os.getenv('POSTGRES_URL'))) as conn:
		with conn.cursor() as cursor:
			cursor.execute('SELECT * FROM metrics_db WHERE type != \'Last 30 Minutes\'')
			
			for row in cursor.fetchall():
				curr_metrics[row[0]] = json.loads(row[1])
	
	curr_metrics['Yesterday']['data_points']['reach'] = yesterday_reach
	curr_metrics['Yesterday']['data_points']['views'] = 286
	
	curr_metrics['All Time']['data_points']['reach'] = all_time_reach
	curr_metrics['All Time']['data_points']['views'] = 5703
	
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
	load_dotenv()
	
	all_time_reach, yesterday_reach, all_time_views = get_data_points()
	
	update_db(all_time_reach, yesterday_reach, all_time_views)

if __name__ == '__main__':
	main()
