import { describe, expect, it } from 'vitest';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { countLinesAsync, countLinesSync } from '../src/lineCounter.js';

const fixture = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'fixtures', 'three-lines.txt');

describe('lineCounter', () => {
  it('sync and async agree on fixture line count', async () => {
    const syncCount = countLinesSync(fixture);
    const asyncCount = await countLinesAsync(fixture);
    expect(syncCount).toBe(3);
    expect(asyncCount).toBe(3);
  });
});
