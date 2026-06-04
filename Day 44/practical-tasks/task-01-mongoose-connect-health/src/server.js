import { createApp } from './app.js';
import { connectMongo } from './db/mongoose.js';

const app = createApp();

// Startup order: load env via imports → connect Mongo → listen HTTP.
await connectMongo();

const port = Number(process.env.PORT || 4401);
app.listen(port, () => {
  console.log(`Day44-task01 listening on http://localhost:${port}`);
});
