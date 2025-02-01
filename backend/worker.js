const redis = require('redis');
const { Pool } = require('pg');

// Redis client
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

// Process requests from the Redis queue
async function processQueue() {
  while (true) {
    const request = await new Promise((resolve) => {
      redisClient.rpop('fridge-queue', (err, data) => {
        if (err) {
          console.error('Error processing queue:', err);
          resolve(null);
        } else {
          resolve(data);
        }
      });
    });

    if (request) {
      const { type, name, quantity } = JSON.parse(request);

      try {
        if (type === 'add') {
          await pgPool.query(`
            INSERT INTO fridge (name, quantity)
            VALUES ($1, $2)
            ON CONFLICT (name) DO UPDATE
            SET quantity = fridge.quantity + $2
          `, [name, quantity]);
        } else if (type === 'update') {
          await pgPool.query('UPDATE fridge SET quantity = $1 WHERE name = $2', [quantity, name]);
        }
        console.log(`Processed ${type} request for ${name}`);
      } catch (err) {
        console.error('Error processing request:', err);
      }
    } else {
      // Wait for a short period before checking the queue again
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  }
}

// Start the worker
processQueue();