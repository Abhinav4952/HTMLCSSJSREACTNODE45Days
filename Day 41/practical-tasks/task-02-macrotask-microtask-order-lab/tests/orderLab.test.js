import { describe, expect, it } from 'vitest';
import { recordExecutionOrder } from '../src/orderLab.js';

describe('orderLab', () => {
  it('matches the taught ordering pattern', async () => {
    const steps = await recordExecutionOrder();
    expect(steps).toEqual(['sync-a', 'sync-b', 'micro-1', 'promise-1', 'timer-1']);
  });
});
