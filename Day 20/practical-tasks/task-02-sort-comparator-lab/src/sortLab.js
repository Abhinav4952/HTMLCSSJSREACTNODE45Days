/**
 * Return a NEW array of strings sorted case-insensitively ascending (A-Z).
 *
 * Rules:
 * - If `words` is not an array, return `null`.
 * - Ignore non-string entries (do not crash).
 * - Sort using `String.prototype.localeCompare` with `{ sensitivity: "base" }`.
 */
export function sortCaseInsensitive(words) {
  if(Array.isArray(words)) return words.filter(word => typeof word==="string").sort((a,b)=>a.localeCompare(b,undefined,{sensitivity: "base"}))

  return null;
}
