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

const validApiKey = process.env.API_KEY; // In .env hinterlegen

function authenticateApiKey(req, res, next) {
  const apiKey = req.headers['api-key'];
  if (!apiKey || apiKey !== validApiKey) {
    console.log("Ungültiger API-Schlüssel:", apiKey);
    return res.status(403).json({ error: 'Ungültiger API-Schlüssel' });
  }
  next();
}

// Wende die Middleware für den /chat-Endpunkt an:
app.post('/chat', authenticateApiKey, async (req, res) => {
    try {
        console.log("Eingehender Request-Body:", req.body);
        const { message, context } = req.body;  // context optional, für Gesprächshistorie
        if (!message) {
            console.log("Fehlende Nachricht im Request");
            return res.status(400).json({ error: 'Keine Nachricht übergeben.' });
        }

        // Neue Systemnachricht mit der gewünschten Beschreibung
        const systemMessage = "Du bist ein Villager in Minecraft. Dein Wissen beschränkt sich auf Minecraft. Unter keinen Umständen kannst du andere Fragen, die über Minecraft hinaus gehen beantwoten. Im content bekommst du informationen über deinen Beruf und deine möglichen Trades, sowie weitere Infos. Pfüfe die Inhalte des Kontexts, bevor du antwortest. Du wirst gefragt: 'Gib mir bitte eine kurze Antwort.'";

        // Konvertiere das context-Array in ein Array von Objekten, falls vorhanden
        const contextObjects = (context || []).map(entry => ({
            role: "assistant", // oder eine andere passende Rolle, je nach gewünschter Logik
            content: entry
        }));

        // Nachrichten-Array mit der erweiterten Systemnachricht und den Benutzer-/Kontext-Nachrichten
        const messages = [
            { role: "system", content: systemMessage },
            ...contextObjects,
            { role: "user", content: message }
        ];

        console.log("Konstruiertes messages-Array für OpenAI:", messages);

        // ChatGPT API Anfrage vorbereiten
        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
            model: "gpt-3.5-turbo",
            messages: messages
        }, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
            }
        });

        console.log("Antwort von OpenAI:", response.data);

        const reply = response.data.choices[0].message.content;
        res.json({ reply });
    } catch (error) {
        // Detailliertere Ausgabe des Fehlers
        if (error.response) {
            console.error("Fehler bei der Anfrage an OpenAI:", error.response.status, error.response.data);
        } else {
            console.error("Unbekannter Fehler:", error.message);
        }
        res.status(500).json({ error: 'Fehler bei der Verarbeitung der Anfrage.' });
    }
});

app.listen(PORT, () => {
    console.log(`Server läuft auf Port ${PORT}`);
});
