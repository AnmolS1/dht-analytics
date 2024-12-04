from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
	DateRange, Dimension, Metric, RunReportRequest, Filter, FilterExpression
)
from dotenv import load_dotenv
import os
import sys
from typing import Literal, Tuple

client = None

def setup() -> Tuple[Tuple[str, Literal['home page form submission']], Tuple[str, Literal['home_buy_now']], Tuple[str, Literal['mango_buy_now_click']], Tuple[str, Literal['rose buy now']]]:
	load_dotenv()
	
	global client
	client = BetaAnalyticsDataClient()
	
	home_form_submit_info = (str(os.getenv('HOME_FORM_SUBMIT_ID')), 'home page form submission')
	home_cta_info = (str(os.getenv('HOME_CTA_ID')), 'home_buy_now')
	mango_cta_info = (str(os.getenv('MANGO_CTA_ID')), 'mango_buy_now_click')
	rose_cta_info = (str(os.getenv('ROSE_CTA_ID')), 'rose buy now')
	
	return home_form_submit_info, home_cta_info, mango_cta_info, rose_cta_info

def retrieve_total_users_given_property(property_id: str) -> int:
	if not client:
		print('The Google Analytics client failed to instantiate.')
		sys.exit(1)
	
	total_users_request = RunReportRequest(
		property=f'properties/{property_id}',
		metrics=[Metric(name='totalUsers')],
		date_ranges=[DateRange(start_date='2024-10-20', end_date='today')],
	)
	
	total_users_response = client.run_report(total_users_request)
	
	return int(total_users_response.rows[0].metric_values[0].value)

def retrieve_total_event_count(property_id: str, event_name: str) -> int:
	if not client:
		print('The Google Analytics client failed to instantiate.')
		sys.exit(1)
	
	cta_event_request = RunReportRequest(
		property=f'properties/{property_id}',
		dimensions=[Dimension(name='eventName')],
		metrics=[Metric(name='eventCount')],
		date_ranges=[DateRange(start_date='2024-10-20', end_date='today')],
		dimension_filter=FilterExpression(
			filter=Filter(
				field_name='eventName',
				string_filter=Filter.StringFilter(value=event_name)
			)
		)
	)
	
	cta_event_response = client.run_report(cta_event_request)
	
	return int(cta_event_response.rows[0].metric_values[0].value)

def do_the_math(home, mango, rose) -> float:
	average_visitors = (home[0] + mango[0] + rose[0]) / 3
	total_fire_count = home[1] + mango[1] + rose[1]
	
	conversion_rate = (total_fire_count / average_visitors) * 100
	
	return conversion_rate

def get_conversion_rate() -> Tuple[str, int]:
	home_form_submit_info, home_cta_info, mango_cta_info, rose_cta_info = setup()
	
	home_form = retrieve_total_users_given_property(home_form_submit_info[0])
	home_cta = (retrieve_total_users_given_property(home_cta_info[0]), retrieve_total_event_count(*home_cta_info))
	mango_cta = (retrieve_total_users_given_property(mango_cta_info[0]), retrieve_total_event_count(*mango_cta_info))
	rose_cta = (retrieve_total_users_given_property(rose_cta_info[0]), retrieve_total_event_count(*rose_cta_info))
	
	conversion_rate = do_the_math(home_cta, mango_cta, rose_cta)
	website_visits = home_form + home_cta[0] + mango_cta[0] + rose_cta[0]
	
	return (f'{conversion_rate:.2f}', website_visits)

if __name__ == '__main__':
	print(f'current conversion rate: {get_conversion_rate()}%')

def get_website_visits_only() -> int:
	info = setup()
	
	home_visits = retrieve_total_users_given_property(info[0][0]) + retrieve_total_users_given_property(info[1][0])
	mango_visits = retrieve_total_users_given_property(info[2][0])
	rose_visits = retrieve_total_users_given_property(info[3][0])
	
	return home_visits + mango_visits + rose_visits
