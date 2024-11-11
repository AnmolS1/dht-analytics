const retrieve_all_time = require("./retrieve-all-time");
const retrieve_yesterday = require("./retrieve-yesterday");

module.exports = async (req, res) => {
	try {
		// Create mock req and res objects if needed
		const mockReq = { method: "GET" }; // You may need to adjust this
		const mockRes = {
			status: (code) => ({ json: (data) => {} }),
			json: (data) => {},
		};

		// Call function1
		await retrieve_all_time(mockReq, mockRes);

		// Call function2
		await retrieve_yesterday(mockReq, mockRes);

		// Send a response from the combined function
		res.status(200).json({
			message: "Both functions executed successfully",
		});
	} catch (error) {
		console.error("Error executing functions:", error);
		res.status(500).json({ error: "Internal server error" });
	}
};
