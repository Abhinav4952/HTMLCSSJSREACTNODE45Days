import { createApp } from './app.js';
import { connectMongo } from './db/mongoose.js';

const app = createApp();
await connectMongo();
const port = Number(process.env.PORT || 4403);
app.listen(port, () => {
  console.log(`Day44-task03 listening on http://localhost:${port}`);
});
