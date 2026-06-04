import { createApp } from './app.js';

const app = createApp();
const port = Number(process.env.PORT || 4003);
app.listen(port, () => {
  console.log(`Day42-task03 listening on http://localhost:${port}`);
});
