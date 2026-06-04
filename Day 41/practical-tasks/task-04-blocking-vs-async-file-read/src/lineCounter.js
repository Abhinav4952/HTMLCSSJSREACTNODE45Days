import fs from 'node:fs';
import fsp from 'node:fs/promises';

/**
 * Counts newline-separated lines using a synchronous read (acceptable for tiny CLIs, risky in servers).
 */
export function countLinesSync(absPath) {
  // TODO(Day41-task04): readFileSync utf8, split on \n, return non-empty trimmed line count (ignore trailing blank line if file ends with newline — match tests).
  throw new Error('TODO(Day41-task04): implement countLinesSync');
}

/**
 * Same behavior as countLinesSync but uses async IO suitable for concurrent servers.
 */
export async function countLinesAsync(absPath) {
  // TODO(Day41-task04): use fs.promises.readFile and mirror sync counting rules.
  throw new Error('TODO(Day41-task04): implement countLinesAsync');
}
