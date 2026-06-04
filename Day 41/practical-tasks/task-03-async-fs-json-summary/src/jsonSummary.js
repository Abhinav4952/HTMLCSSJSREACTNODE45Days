import fs from 'node:fs/promises';

/**
 * Reads JSON from disk, expects a top-level array of objects with string `title`.
 * @param {string} absPath absolute path to UTF-8 JSON file
 * @returns {Promise<{ count: number, titles: string[] }>}
 */
export async function summarizeJsonArrayFile(absPath) {
  // TODO(Day41-task03): read file with fs.promises, JSON.parse, validate shape, return summary.
  throw new Error('TODO(Day41-task03): implement summarizeJsonArrayFile');
}
