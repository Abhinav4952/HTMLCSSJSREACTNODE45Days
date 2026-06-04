import { createApp } from './app.js';

const app = createApp();
const port = Number(process.env.PORT || 4004);
app.listen(port, () => {
  console.log(`Day42-task04 listening on http://localhost:${port}`);
});
