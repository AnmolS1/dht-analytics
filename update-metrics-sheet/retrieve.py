from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
	DateRange, Dimension, Metric, RunReportRequest, Filter, FilterExpression
)
from typing import Any
from custom_types import Property
import sys

client = None

def retrieve_given_date_range(start: str, end: str, properties: Property) -> dict[str, Any]:
	if not client:
		print('welp')
		sys.exit(1)
	
	data = {
		'conversion': 0,
		'bounce': 0,
		'engagement': 0,
		'visits': 0,
		'countryCount': [],
		'cta_clicks': 0,
		'visitors': 0,
		'engagements': 0
	}
	
	country_idx_manager = {}
	for property in properties:
		metrics = [
			Metric(name='bounceRate'),
			Metric(name='userEngagementDuration'),
			Metric(name='screenPageViews'),
			Metric(name='activeUsers'),
			Metric(name='engagedSessions')
		]
		
		metric_requests = [
			RunReportRequest(
				property=f'properties/{property[0]}',
				metrics=metrics,
				date_ranges=[DateRange(start_date=start, end_date=end)],
			),
			RunReportRequest(
				property=f'properties/{property[0]}',
				metrics=[Metric(name='activeUsers')],
				date_ranges=[DateRange(start_date=start, end_date=end)],
				dimensions=[Dimension(name='country')]
			)
		]
		
		if len(property) == 2:
			metric_requests.append(
				RunReportRequest(
					property=f'properties/{property[0]}',
					metrics=[Metric(name='eventCount')],
					date_ranges=[DateRange(start_date=start, end_date=end)],
					dimension_filter=FilterExpression(
						filter=Filter(
							field_name='eventName',
							string_filter=Filter.StringFilter(value=property[1])
						)
					)
				)
			)
		
		metric_responses = [client.run_report(request) for request in metric_requests]
		
		if metric_responses[0].rows:
			metric_info = metric_responses[0].rows[0].metric_values
			
			data['bounce'] += float(metric_info[0].value)
			data['engagement'] += float(metric_info[1].value)
			data['visits'] += int(metric_info[2].value)
			data['visitors'] += int(metric_info[3].value)
			data['engagements'] += int(metric_info[4].value)
		
		if len(property) == 2 and metric_responses[2].rows:
			data['cta_clicks'] += int(metric_responses[2].rows[0].metric_values[0].value)
		
		country_info = metric_responses[1].rows
		for country in country_info:
			ctry = 'Unknown' if country.dimension_values[0].value == '(not set)' else country.dimension_values[0].value
			
			if ctry in country_idx_manager:
				data['countryCount'][country_idx_manager[ctry]]['count'] += int(country.metric_values[0].value)
			else:
				data['countryCount'].append({'country': ctry, 'count': int(country.metric_values[0].value)})
				country_idx_manager[ctry] = len(data['countryCount']) - 1
	
	data['bounce'] = data['bounce'] / 4
	data['visits'] = round(data['visits'] / 4)
	data['visitors'] = round(data['visitors'] / 4)
	data['engagements'] = round(data['engagements'] / 4)
	for i in range(len(data['countryCount'])):
		data['countryCount'][i]['count'] = round(data['countryCount'][i]['count'] / 4)
	
	data['engagement'] = round((data['engagement'] / 4) / data['visitors']) if data['visitors'] != 0 else 0
	data['conversion'] = data['cta_clicks'] / data['visitors'] if data['visitors'] != 0 else 0
	
	return data

def retrieve_yesterday(properties: Property) -> dict[str, Any]:
	return retrieve_given_date_range('1daysAgo', '1daysAgo', properties)

def retrieve_all_time(properties: Property) -> dict[str, Any]:
	return retrieve_given_date_range('2024-10-21', '1daysAgo', properties)

def retrieve(properties: Property):
	global client
	client = BetaAnalyticsDataClient()
	
	return retrieve_yesterday(properties), retrieve_all_time(properties)
