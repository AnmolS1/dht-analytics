const { sql } = require('@vercel/postgres');

module.exports = async (req, res) => {
	if (req.method !== 'POST') {
		return res.status(405).json({ error: "Method Not Allowed" });
	}

	try {
		const { type } = req.body;

		if (!type) {
			return res.status(400).json({ error: "Type is required" });
		}

		const result = await sql`
			SELECT * FROM metrics_db
			WHERE type = ${type}
		`;
		
		if (result.rows.length != 1) {
			return res.status(400).json({ error: "Did not find correct data" });
		}

		res.status(200).json(result.rows[0]['data']);
	} catch (error) {
		console.error('Error retrieving data:', error);
		res.status(500).json({ error: 'Error retrieving data' });
	}
};