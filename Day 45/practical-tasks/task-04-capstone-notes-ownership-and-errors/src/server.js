import { createApp } from './app.js';
import { connectMongo } from './db/mongoose.js';

const app = createApp();
await connectMongo();
const port = Number(process.env.PORT || 4504);
app.listen(port, () => {
  console.log(`Day45-task04 listening on http://localhost:${port}`);
});
