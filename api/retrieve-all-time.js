const { BetaAnalyticsDataClient } = require("@google-analytics/data");
const { sql } = require("@vercel/postgres");

module.exports = async (req, res) => {
	if (req.method !== "GET") {
		return res.status(405).json({ error: "Method Not Allowed" });
	}

	const all_time = {
		metrics: {
			ctr: 0,
			conversion: 0,
			bounce: 0,

			engagement: 0,
			visits: 0,
			countryCount: [],
		},
		data_points: {
			cta_clicks: 0,
			visitors: 0,
			engagements: 0,
			reach: 0,
		},
	};

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
					dateRanges: [{ startDate: "2023-10-19", endDate: "today" }],
					metrics: metrics,
				}),
				analyticsDataClient.runReport({
					property: `properties/${property["id"]}`,
					dateRanges: [{ startDate: "2023-10-19", endDate: "today" }],
					metrics: [{ name: "activeUsers" }],
					dimensions: [{ name: "country" }],
				}),
			];

			if (property["event_name"] !== "") {
				metric_requests.push(
					analyticsDataClient.runReport({
						property: `properties/${property["id"]}`,
						dateRanges: [
							{ startDate: "2023-10-19", endDate: "today" },
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

			all_time.metrics.bounce += parseFloat(metric_info[0].value);
			all_time.metrics.engagement += parseFloat(metric_info[1].value);
			all_time.metrics.visits += parseInt(metric_info[2].value);
			all_time.data_points.visitors += parseInt(metric_info[3].value);
			all_time.data_points.engagements += parseInt(metric_info[4].value);
			all_time.data_points.cta_clicks +=
				property["event_name"] !== ""
					? parseInt(all_metrics[2][0].rows[0].metricValues[0].value)
					: 0;

			const country_info = all_metrics[1][0].rows;
			for (let country of country_info) {
				var ctry =
					country.dimensionValues[0].value === "(not set)"
						? "Unknown"
						: country.dimensionValues[0].value;

				if (Object.keys(country_idx_manager).includes(ctry)) {
					all_time.metrics.countryCount[
						country_idx_manager[ctry]
					].count += parseInt(country.metricValues[0].value);
				} else {
					all_time.metrics.countryCount.push({
						country: ctry,
						count: parseInt(country.metricValues[0].value),
					});
					country_idx_manager[ctry] =
						all_time.metrics.countryCount.length - 1;
				}
			}
		}

		all_time.metrics.bounce = Math.round(
			(all_time.metrics.bounce / 4) * 100,
		);
		all_time.metrics.visits = Math.round(all_time.metrics.visits / 4);
		all_time.data_points.visitors = Math.round(
			all_time.data_points.visitors / 4,
		);
		all_time.data_points.engagements = Math.round(
			all_time.data_points.engagements / 4,
		);
		for (let i = 0; i < all_time.metrics.countryCount.length; i++) {
			all_time.metrics.countryCount[i].count = Math.round(
				all_time.metrics.countryCount[i].count / 4,
			);
		}

		all_time.metrics.engagement =
			all_time.data_points.visitors != 0
				? Math.round(
						all_time.metrics.engagement /
							4 /
							all_time.data_points.visitors,
					)
				: 0;
		all_time.metrics.conversion =
			all_time.data_points.visitors != 0
				? Math.round(
						(all_time.data_points.cta_clicks /
							all_time.data_points.visitors) *
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
			SET data = ${JSON.stringify(all_time)}::jsonb
			WHERE type = 'All Time'
		`;
	} catch (error) {
		console.error("Error updating data:", error);
		res.status(500).json({ error: "Error updating data" });
	}

	res.status(200).json(all_time);
};
