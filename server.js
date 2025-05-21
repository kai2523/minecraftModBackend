// server.js
require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3000;
app.use(bodyParser.json());

app.get('/', (_, res) => res.send('Minecraft Chat Backend ist aktiv!'));

// API-Key Auth
const validApiKey = process.env.API_KEY;
function authenticateApiKey(req, res, next) {
  const apiKey = req.headers['api-key'];
  if (!apiKey || apiKey !== validApiKey) {
    console.log('Ungültiger API-Schlüssel:', apiKey);
    return res.status(403).json({ error: 'Ungültiger API-Schlüssel' });
  }
  next();
}

// Sentiment→Prompt mapping
function mapLabel(label) {
  switch (label.toLowerCase()) {
    case 'freundlich': return 'Antworte im sehr freundlichen, enthusiastischen Ton.';
    case 'neutral': return 'Antworte in neutralem Ton.';
    case 'unfreundlich': return 'Antworte im sehr unfreundlichen, schroffen Ton mit beleidigenden Ausdrücken.';
    default: return 'Antworte in neutralem Ton.';
  }
}

// Lade die Transformers.js–Pipeline einmal beim Start
let sentimentPipeline;
const pipelineReady = (async () => {
  const { pipeline, env } = await import('@huggingface/transformers');

  // erlaube lokale Model-Ordner
  env.allowLocalModels = true;

  sentimentPipeline = await pipeline(
    'sentiment-analysis',
    './tinybert-german-finetuned',
    { provider: 'wasm', use_safetensors: true }
  );

  console.log('Sentiment-Pipeline (TinyBERT-German) geladen.');
})();

app.post('/chat', authenticateApiKey, async (req, res) => {
  try {
    await pipelineReady;

    const { message, context } = req.body;
    if (!message) return res.status(400).json({ error: 'Keine Nachricht übergeben.' });

    // 1) Sentiment
    const [{ label: starLabel, score }] = await sentimentPipeline(message);
    console.log('Prompt:', message);
    console.log(`Sentiment-Rating: ${starLabel} (${(score * 100).toFixed(1)}%)`);
    const sentimentPrompt = mapLabel(starLabel);

    // 2) System-Prompt für OpenAI
    const systemMessage = `
Du bist ein Villager in Minecraft. Dein Wissen beschränkt sich auf Minecraft.
Unter keinen Umständen beantwortest du Fragen außerhalb dieses Themas.
Prüfe den Kontext, bevor du antwortest. ${sentimentPrompt}
Gib mir bitte eine kurze Antwort.
    `.trim();

    const messages = [
      { role: 'system', content: systemMessage },
      { role: 'assistant', content: (context || []).join('\n') },
      { role: 'user', content: message }
    ];

    // 3) Anfrage an OpenAI Chat-Endpoint
    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      { model: 'gpt-3.5-turbo', messages, temperature: 0.7 },
      { headers: { Authorization: `Bearer ${process.env.OPENAI_API_KEY}` } }
    );

    const reply = response.data.choices[0].message.content;
    console.log('Antwort an Client:', reply);
    res.json({ reply });

  } catch (error) {
    console.error('Fehler im /chat Handler:', error);
    res.status(500).json({ error: 'Fehler bei der Verarbeitung der Anfrage.' });
  }
});

app.listen(PORT, () => console.log(`Server läuft auf Port ${PORT}`));
