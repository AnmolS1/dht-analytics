const { BetaAnalyticsDataClient } = require("@google-analytics/data");
const { sql } = require("@vercel/postgres");

module.exports = async (req, res) => {
	if (req.method !== "GET") {
		return res.status(405).json({ error: "Method Not Allowed" });
	}

	const last_30_minutes = {
		metrics: {
			conversion: 0,
			bounce: 0,

			visits: 0,
			countryCount: [],
		},
		data_points: {
			cta_clicks: 0,
			visitors: 0,
			engagements: 0,
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
			const last_30_minutes_metrics = await Promise.all([
				analyticsDataClient.runRealtimeReport({
					property: `properties/${property["id"]}`,
					metrics: [{ name: "screenPageViews" }],
				}),
				analyticsDataClient.runRealtimeReport({
					property: `properties/${property["id"]}`,
					metrics: [{ name: "eventcount" }],
					dimensions: [{ name: "eventName" }],
				}),
				analyticsDataClient.runRealtimeReport({
					property: `properties/${property["id"]}`,
					metrics: [{ name: "activeUsers" }],
					dimensions: [{ name: "country" }],
				}),
			]);

			if (last_30_minutes_metrics[0][0].rows.length > 0) {
				const metric_info =
					last_30_minutes_metrics[0][0].rows[0].metricValues;

				last_30_minutes.metrics.visits += parseInt(
					metric_info[0].value,
				);
			}

			if (last_30_minutes_metrics[1][0].rows.length > 0) {
				for (let metric of last_30_minutes_metrics[1][0].rows) {
					if (metric.dimensionValues[0].value === "user_engagement") {
						last_30_minutes.data_points.engagements += parseInt(
							metric.metricValues[0].value,
						);
					} else if (
						metric.dimensionValues[0].value ===
						property["event_name"]
					) {
						last_30_minutes.data_points.cta_clicks += parseInt(
							metric.metricValues[0].value,
						);
					} else if (
						metric.dimensionValues[0].value === "page_view"
					) {
						last_30_minutes.data_points.visitors += parseInt(
							metric.metricValues[0].value,
						);
					}
				}
			}

			if (last_30_minutes_metrics[2][0].rows.length > 0) {
				for (let country of last_30_minutes_metrics[2][0].rows) {
					var ctry =
						country.dimensionValues[0].value === "(not set)"
							? "Unknown"
							: country.dimensionValues[0].value;

					if (Object.keys(country_idx_manager).includes(ctry)) {
						last_30_minutes.metrics.countryCount[
							country_idx_manager[ctry]
						].count += parseInt(country.metricValues[0].value);
					} else {
						last_30_minutes.metrics.countryCount.push({
							country: ctry,
							count: parseInt(country.metricValues[0].value),
						});
						country_idx_manager[ctry] =
							last_30_minutes.metrics.countryCount.length - 1;
					}
				}
			}
		}

		last_30_minutes.metrics.visits = Math.round(
			last_30_minutes.metrics.visits / 4,
		);
		last_30_minutes.data_points.visitors = Math.round(
			last_30_minutes.data_points.visitors / 4,
		);
		last_30_minutes.data_points.engagements = Math.round(
			last_30_minutes.data_points.engagements / 4,
		);
		for (let i = 0; i < last_30_minutes.metrics.countryCount.length; i++) {
			last_30_minutes.metrics.countryCount[i].count = Math.round(
				last_30_minutes.metrics.countryCount[i].count / 4,
			);
		}

		last_30_minutes.metrics.bounce =
			last_30_minutes.data_points.visitors != 0
				? Math.round(
						((last_30_minutes.data_points.visitors -
							last_30_minutes.data_points.engagements) /
							last_30_minutes.data_points.visitors) *
							100,
					)
				: 0;
		last_30_minutes.metrics.conversion =
			last_30_minutes.data_points.visitors != 0
				? Math.round(
						(last_30_minutes.data_points.cta_clicks /
							last_30_minutes.data_points.visitors) *
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
			SET data = ${JSON.stringify(last_30_minutes)}::jsonb
			WHERE type = 'Last 30 Minutes'
		`;
	} catch (error) {
		console.error("Error updating data:", error);
		res.status(500).json({ error: "Error updating data" });
	}

	res.status(200).json(last_30_minutes);
};
