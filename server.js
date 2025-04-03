// server.js
require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.send('Minecraft Chat Backend ist aktiv!');
});

app.post('/chat', async (req, res) => {
    try {
        const { message, context } = req.body;  // context optional, für Gesprächshistorie
        if (!message) {
            return res.status(400).json({ error: 'Keine Nachricht übergeben.' });
        }

        // ChatGPT API Anfrage vorbereiten
        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
            model: "gpt-3.5-turbo",
            messages: [
                { role: "system", content: "Du bist ein hilfreicher Dorfbewohner." },
                ...context || [],
                { role: "user", content: message }
            ]
        }, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
            }
        });

        const reply = response.data.choices[0].message.content;
        res.json({ reply });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Fehler bei der Verarbeitung der Anfrage.' });
    }
});

app.listen(PORT, () => {
    console.log(`Server läuft auf Port ${PORT}`);
});
