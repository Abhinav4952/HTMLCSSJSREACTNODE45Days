/**
 * Records a deliberately ordered sequence of labels.
 * Fix the registration order so microtasks drain before the macrotimer fires,
 * and `queueMicrotask` runs before the Promise reaction (FIFO within microtasks).
 */
export async function recordExecutionOrder() {
  const steps = [];
  const log = (label) => steps.push(label);

  log('sync-a');

  // TODO(Day41-task02): reorder the next three registrations so tests pass.
  // Current (wrong) order is Promise microtask before queueMicrotask — swap as needed.
  setTimeout(() => log('timer-1'), 0);
  Promise.resolve().then(() => log('promise-1'));
  queueMicrotask(() => log('micro-1'));

  log('sync-b');

  await new Promise((resolve) => setTimeout(resolve, 0));
  return steps;
}
