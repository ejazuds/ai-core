const cds = require('@sap/cds');
const axios = require('axios');

// 🔹 Hardcoded UAA Credentials
const UAA_URL = "";
const CLIENT_ID = "";
const CLIENT_SECRET = "";

// 🔹 AI Core Endpoint
const resourceGroupId = ``
const AI_CORE_URL = "";

// Function to fetch AI Core token
const getAccessToken = async () => {
    try {
        const response = await axios.post(
            UAA_URL,
            new URLSearchParams({
                grant_type: "client_credentials",
                client_id: CLIENT_ID,
                client_secret: CLIENT_SECRET,
            }),
            { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
        );

        return response.data.access_token;
    } catch (error) {
        console.error("❌ Error fetching AI Core token:", error.message);
        throw new Error("Failed to get AI Core token");
    }
};


module.exports = cds.service.impl(async function () {
    const { ChatResponse } = this.entities;

    this.on('askLLM', async (req) => {
        const { query } = req.data;

        if (!query) return req.reject(400, "Query is required");

        try {
            const token = await getAccessToken();

           console.log(query)

           const data = {
            messages: [{ role: "user", content: query }],
            max_tokens: 4000,
            temperature: 0.0,
        };
            const response = await axios.post(
                AI_CORE_URL,
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                        "AI-Resource-Group": resourceGroupId
                    },
                }
            );

            const output = response.data.choices[0].message.content;
            let llmResponse = JSON.parse(output);
             console.log(llmResponse)
             //fetch country
             console.log(llmResponse.country)


            // Save response (optional)
            const newEntry = await INSERT.into(ChatResponse).entries([
                { id: cds.utils.uuid(), query, response: llmResponse.country }
            ]);

           return newEntry[0];
        } catch (error) {
            console.error("❌ AI Core Error:", error.message);
            return req.reject(500, "AI Core request failed");
        }
    });
});
