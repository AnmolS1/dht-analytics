import psycopg, json

def update_db(data, db_url):
	curr_metrics = {}
	
	with psycopg.connect(db_url) as conn:
		with conn.cursor() as cursor:
			cursor.execute('SELECT * FROM metrics_db WHERE type != \'Last 30 Minutes\'')
			
			for row in cursor.fetchall():
				curr_metrics[row[0]] = json.loads(row[1])
	
	curr_metrics['Yesterday']['data_points']['reach'] = data['yday_reach']
	curr_metrics['Yesterday']['data_points']['views'] = data['yday_views']
	curr_metrics['Yesterday']['metrics']['uctr'] = round((curr_metrics['Yesterday']['data_points']['visitors'] / curr_metrics['Yesterday']['data_points']['reach']) * 100)
	curr_metrics['Yesterday']['metrics']['gctr'] = round((curr_metrics['Yesterday']['metrics']['visits'] / curr_metrics['Yesterday']['data_points']['views']) * 100)
	
	curr_metrics['All Time']['data_points']['reach'] = data['all_time_reach']
	curr_metrics['All Time']['data_points']['views'] = data['all_time_views']
	curr_metrics['All Time']['metrics']['uctr'] = round((curr_metrics['All Time']['data_points']['visitors'] / curr_metrics['All Time']['data_points']['reach']) * 100)
	curr_metrics['All Time']['metrics']['gctr'] = round((curr_metrics['All Time']['metrics']['visits'] / curr_metrics['All Time']['data_points']['views']) * 100)
	
	with psycopg.connect(db_url) as conn:
		with conn.cursor() as cursor:
			query = "UPDATE metrics_db SET data = %s::jsonb WHERE type = %s"
			
			cursor.execute(query, (json.dumps(curr_metrics["Yesterday"]), 'Yesterday'))
			cursor.execute(query, (json.dumps(curr_metrics["All Time"]), 'All Time'))
			
			conn.commit()
