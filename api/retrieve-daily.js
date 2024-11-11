const retrieve_all_time = require("./retrieve-all-time");
const retrieve_yesterday = require("./retrieve-yesterday");
const retrieve_last_30 = require("./retrieve-last-30-minutes");

module.exports = async (req, res) => {
	try {
		const mockReq = { method: "GET" };
		const mockRes = {
			status: (code) => ({ json: (data) => {} }),
			json: (data) => {},
		};

		await retrieve_all_time(mockReq, mockRes);
		await retrieve_yesterday(mockReq, mockRes);
		await retrieve_last_30(mockReq, mockRes);

		res.status(200).json({
			message: "All functions executed successfully",
		});
	} catch (error) {
		console.error("Error executing functions:", error);
		res.status(500).json({ error: "Internal server error" });
	}
};
