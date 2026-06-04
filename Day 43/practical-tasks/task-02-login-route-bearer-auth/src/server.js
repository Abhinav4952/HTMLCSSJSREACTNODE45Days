import { createApp } from './app.js';

const app = createApp();
const port = Number(process.env.PORT || 4302);
app.listen(port, () => {
  console.log(`Day43-task02 listening on http://localhost:${port}`);
});
