import { createApp } from './app.js';

const app = createApp();
const port = Number(process.env.PORT || 4001);
app.listen(port, () => {
  console.log(`Day42-task01 listening on http://localhost:${port}`);
});
