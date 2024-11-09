const { BetaAnalyticsDataClient } = require('@google-analytics/data');

module.exports = async (req, res) => {
	if (req.method !== 'GET') {
		return res.status(405).json({ error: "Method Not Allowed" });
	}

	try {
		const ga4_creds = JSON.parse(process.env.GOOGLE_APPLICATION_CREDENTIALS)

		const analyticsDataClient = new BetaAnalyticsDataClient({
			credentials: {
				client_email: ga4_creds['client_email'],
				private_key: ga4_creds['private_key']
			}
		});

		const [response] = await analyticsDataClient.runReport({
			property: `properties/${process.env.MANGO_CTA_ID}`,
			dateRanges: [
				{
					startDate: '30daysAgo',
					endDate: 'today',
				},
			],
			metrics: [
				{
					name: 'screenPageViews',
				},
				{
					name: 'sessions',
				},
			],
		});

		const formattedResponse = {
			screenPageViews: response.rows[0].metricValues[0].value,
			sessions: response.rows[0].metricValues[1].value
		};

		res.status(200).json(formattedResponse);
	} catch (error) {
		console.error('Error fetching Google Analytics data:', error);
		res.status(500).json({ error: 'Failed to fetch data' });
	}
};