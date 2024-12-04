const { BetaAnalyticsDataClient } = require("@google-analytics/data");
const { sql } = require("@vercel/postgres");

module.exports = async (req, res) => {
	if (req.method !== "GET") {
		return res.status(405).json({ error: "Method Not Allowed" });
	}

	const yesterday = {};

	try {
		yesterday =
			await sql`SELECT * FROM metrics_db WHERE type = 'Yesterday'`;
	} catch (error) {
		console.error("Error retrieving data:", error);
		res.status(500).json({ error: "Error retrieving data" });
	}

	yesterday.metrics.conversion = 0;
	yesterday.metrics.bounce = 0;
	yesterday.metrics.engagement = 0;
	yesterday.metrics.visits = 0;
	yesterday.metrics.countryCount = [];
	yesterday.data_points.cta_clicks = 0;
	yesterday.data_points.visitors = 0;
	yesterday.data_points.engagements = 0;

	try {
		const ga4_creds = JSON.parse(
			process.env.GOOGLE_APPLICATION_CREDENTIALS,
		);
		const properties = process.env.GA4_INFO.split("|").map((e) =>
			JSON.parse(e),
		);

		const analyticsDataClient = new BetaAnalyticsDataClient({
			credentials: {
				client_email: ga4_creds["client_email"],
				private_key: ga4_creds["private_key"],
			},
		});

		let country_idx_manager = {};

		for (let property of properties) {
			const metrics = [
				{ name: "bounceRate" },
				{ name: "userEngagementDuration" },
				{ name: "screenPageViews" },
				{ name: "activeUsers" },
				{ name: "engagedSessions" },
			];

			const metric_requests = [
				analyticsDataClient.runReport({
					property: `properties/${property["id"]}`,
					dateRanges: [
						{
							startDate: "1daysAgo",
							endDate: "1daysAgo",
						},
					],
					metrics: metrics,
				}),
				analyticsDataClient.runReport({
					property: `properties/${property["id"]}`,
					dateRanges: [
						{
							startDate: "1daysAgo",
							endDate: "1daysAgo",
						},
					],
					metrics: [{ name: "activeUsers" }],
					dimensions: [{ name: "country" }],
				}),
			];

			if (property["event_name"] !== "") {
				metric_requests.push(
					analyticsDataClient.runReport({
						property: `properties/${property["id"]}`,
						dateRanges: [
							{
								startDate: "1daysAgo",
								endDate: "1daysAgo",
							},
						],
						metrics: [{ name: "eventCount" }],
						dimensionFilter: {
							filter: {
								fieldName: "eventName",
								stringFilter: {
									matchType: "EXACT",
									value: `${property["event_name"]}`,
								},
							},
						},
					}),
				);
			}

			const all_metrics = await Promise.all(metric_requests);

			const metric_info = all_metrics[0][0].rows[0].metricValues;

			yesterday.metrics.bounce += parseFloat(metric_info[0].value);
			yesterday.metrics.engagement += parseFloat(metric_info[1].value);
			yesterday.metrics.visits += parseInt(metric_info[2].value);
			yesterday.data_points.visitors += parseInt(metric_info[3].value);
			yesterday.data_points.engagements += parseInt(metric_info[4].value);
			yesterday.data_points.cta_clicks +=
				property["event_name"] !== "" &&
				all_metrics[2][0].rows.length > 0
					? parseInt(all_metrics[2][0].rows[0].metricValues[0].value)
					: 0;

			const country_info = all_metrics[1][0].rows;
			for (let country of country_info) {
				var ctry =
					country.dimensionValues[0].value === "(not set)"
						? "Unknown"
						: country.dimensionValues[0].value;

				if (Object.keys(country_idx_manager).includes(ctry)) {
					yesterday.metrics.countryCount[
						country_idx_manager[ctry]
					].count += parseInt(country.metricValues[0].value);
				} else {
					yesterday.metrics.countryCount.push({
						country: ctry,
						count: parseInt(country.metricValues[0].value),
					});
					country_idx_manager[ctry] =
						yesterday.metrics.countryCount.length - 1;
				}
			}
		}

		yesterday.metrics.bounce = Math.round(
			(yesterday.metrics.bounce / 4) * 100,
		);
		yesterday.metrics.visits = Math.round(yesterday.metrics.visits / 4);
		yesterday.data_points.visitors = Math.round(
			yesterday.data_points.visitors / 4,
		);
		yesterday.data_points.engagements = Math.round(
			yesterday.data_points.engagements / 4,
		);
		for (let i = 0; i < yesterday.metrics.countryCount.length; i++) {
			yesterday.metrics.countryCount[i].count = Math.round(
				yesterday.metrics.countryCount[i].count / 4,
			);
		}

		yesterday.metrics.engagement =
			yesterday.data_points.visitors != 0
				? Math.round(
						yesterday.metrics.engagement /
							4 /
							yesterday.data_points.visitors,
					)
				: 0;
		yesterday.metrics.conversion =
			yesterday.data_points.visitors != 0
				? Math.round(
						(yesterday.data_points.cta_clicks /
							yesterday.data_points.visitors) *
							100,
					)
				: 0;
	} catch (error) {
		console.error("Error fetching Google Analytics data:", error);
		res.status(500).json({ error: "Failed to fetch data" });
	}

	try {
		await sql`
			UPDATE metrics_db
			SET data = ${JSON.stringify(yesterday)}::jsonb
			WHERE type = 'Yesterday'
		`;
	} catch (error) {
		console.error("Error updating data:", error);
		res.status(500).json({ error: "Error updating data" });
	}

	res.status(200).json(yesterday);
};
