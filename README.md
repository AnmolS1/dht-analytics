# DrinkHumTum Analytics Unmanned Node (DAmN)
#### This collection of scripts (and soon website) leverages the GA4 API and Selenium to grab data across DrinkHumTum's socials and Google metrics. These data are then analyzed to produce KPI values.

## Usage

### v1

1. Install [python](https://www.python.org/) if not already installed
2. Install the requirements by running `chmod u+x setup.sh && ./setup.sh` on a Mac or `setup.bat` on Windows
3. Get the environment variables by asking me for it and put the file in `v1` under the name `.env`
4. Get credentials for GA4 by asking me for it and put the credentials file in `v1` with the name `credentials.json`
5. Download the correct chromedriver for your version of Chrome by following instructions [here](https://developer.chrome.com/docs/chromedriver/downloads#current_releases) and put the chromedriver executable in `v1` under the name `chromedriver`
6. You may ignore the previous instructions and just ask me if you don't want to do it.
7. Access `v1` in your file explorer. Right click on the folder and either click "New Terminal at Folder" on a Mac or "Git Bash Here" on Windows
8. Get the metrics by running `./get_metrics` on a Mac or `get_metrics.bat` on Windows

## Coming Updates

- use Instagram API instead of Selenium
	- requirements: LLC for business verification through Meta, 2 days for implementation
	- challenges: none
	- benefits: minimum 4x speed improvement, functionality in server-side JS through Vercel deployments
- basic web-based dashboard to display metrics
	- requirements: Instagram API update
	- challenges: time factor
	- benefits: easy-to-use, no extraneous installations or setup required
