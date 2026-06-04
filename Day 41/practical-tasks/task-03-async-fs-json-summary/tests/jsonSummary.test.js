import { describe, expect, it } from 'vitest';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { summarizeJsonArrayFile } from '../src/jsonSummary.js';

const fixture = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'fixtures', 'items.json');

describe('jsonSummary', () => {
  it('summarizes titles and count', async () => {
    const summary = await summarizeJsonArrayFile(fixture);
    expect(summary).toEqual({
      count: 3,
      titles: ['Alpha', 'Beta', 'Gamma'],
    });
  });

  it('rejects non-array JSON', async () => {
    const notArray = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'fixtures', 'object.json');
    await expect(summarizeJsonArrayFile(notArray)).rejects.toThrow(/array/i);
  });
});
