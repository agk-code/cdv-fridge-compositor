const express = require('express');
const redis = require('redis');
const { Pool } = require('pg');

const app = express();
app.use(express.json());

// Redis client for queueing
const redisClient = redis.createClient({
  host: process.env.REDIS_HOST || 'pepperoni',
  port: process.env.REDIS_PORT || 6379
});
redisClient.on('error', (err) => console.error('Redis error:', err));

// PostgreSQL client
const pgPool = new Pool({
  user: process.env.POSTGRES_USER || 'postgres',
  host: process.env.POSTGRES_HOST || 'mushroom',
  database: process.env.POSTGRES_DB || 'fridge',
  password: process.env.POSTGRES_PASSWORD || 'postgres',
  port: 5432
});

// Initialize database table
async function initDB() {
  await pgPool.query(`
    CREATE TABLE IF NOT EXISTS fridge (
      name TEXT PRIMARY KEY,
      quantity INT NOT NULL
    )
  `);
}

// Get all items in the fridge
app.get('/api/fridge', async (req, res) => {
  const result = await pgPool.query('SELECT * FROM fridge');
  res.json(result.rows);
});

// Add or update an item in the fridge (queue the request in Redis)
app.post('/api/fridge', async (req, res) => {
  const { name, quantity } = req.body;
  const request = { type: 'add', name, quantity };
  redisClient.lpush('fridge-queue', JSON.stringify(request), (err) => {
    if (err) {
      console.error('Error queuing request:', err);
      res.status(500).send('Error queuing request');
    } else {
      res.sendStatus(200);
    }
  });
});

// Update item quantity (queue the request in Redis)
app.put('/api/fridge/:name', async (req, res) => {
  const { name } = req.params;
  const { quantity } = req.body;
  const request = { type: 'update', name, quantity };
  redisClient.lpush('fridge-queue', JSON.stringify(request), (err) => {
    if (err) {
      console.error('Error queuing request:', err);
      res.status(500).send('Error queuing request');
    } else {
      res.sendStatus(200);
    }
  });
});

// Start the server
async function start() {
  await initDB();
  app.listen(3000, () => console.log('Backend running on http://localhost:3000'));
}

start();