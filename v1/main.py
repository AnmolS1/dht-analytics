from get_conversion_rate import get_conversion_rate
from get_click_thru_rate import get_click_thru_rate

def main():
	conversion_rate, website_visits = get_conversion_rate()
	print(f'current conversion rate:    {conversion_rate}%')
	
	click_thru_rate = get_click_thru_rate(website_visits)
	print(f'current click through rate: {click_thru_rate}%')

if __name__ == '__main__':
	main()
