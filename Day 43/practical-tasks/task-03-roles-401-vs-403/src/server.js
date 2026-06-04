import { createApp } from './app.js';

const app = createApp();
const port = Number(process.env.PORT || 4303);
app.listen(port, () => {
  console.log(`Day43-task03 listening on http://localhost:${port}`);
});
