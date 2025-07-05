// index.js
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import OpenAI from 'openai';

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

// Demo stub to avoid empty results when you’re out of tokens
const DEMO_ITINERARY = `
Day 1: Rotorua thermal parks; Maori cultural show  
Day 2: Lake Tarawera boat cruise; local craft markets
`.trim();

// Initialize OpenAI
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

app.post('/itineraries', async (req, res) => {
  const { location, days, interests, language, pace } = req.body;
  const prompt = `
You are a concise NZ travel-bot. Generate a ${days}-day itinerary in ${location}, 
interests: ${interests.join(', ')}, output in ${language}, pace: ${pace}. 
Keep it under 150 tokens, use bullet points.
`.trim();

  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [
        { role: 'system', content: 'You generate very concise travel itineraries.' },
        { role: 'user',  content: prompt }
      ],
      temperature: 0.3,
      max_tokens: 150
    });

    const text = response.choices[0].message.content.trim();
    res.json({ itinerary: text });

  } catch (err) {
    console.error('OpenAI error:', err.status, err.message);
    if (err.status === 429) {
      // out of quota – return demo stub
      return res.json({ itinerary: DEMO_ITINERARY });
    }
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () =>
  console.log(`Server listening on http://localhost:${PORT}`)
);