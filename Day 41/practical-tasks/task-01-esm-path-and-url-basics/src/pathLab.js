import path from 'node:path';
import { fileURLToPath } from 'node:url';

/**
 * Returns the absolute path to this module's directory (ESM equivalent of __dirname).
 */
export function moduleDirname(importMetaUrl) {
  // TODO(Day41-task01): Use fileURLToPath + path.dirname to return the directory containing this file.
  throw new Error('TODO(Day41-task01): implement moduleDirname');
}

/**
 * Joins path segments after resolving them relative to this module file's directory.
 * @param {string} importMetaUrl - pass import.meta.url from the caller
 * @param {...string} segments
 */
export function joinRelativeToModule(importMetaUrl, ...segments) {
  // TODO(Day41-task01): Join moduleDirname(importMetaUrl) with segments using path.join.
  throw new Error('TODO(Day41-task01): implement joinRelativeToModule');
}
