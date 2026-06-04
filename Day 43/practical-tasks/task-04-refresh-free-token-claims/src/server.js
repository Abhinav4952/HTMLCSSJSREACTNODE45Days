import { createApp } from './app.js';

const app = createApp();
const port = Number(process.env.PORT || 4304);
app.listen(port, () => {
  console.log(`Day43-task04 listening on http://localhost:${port}`);
});
