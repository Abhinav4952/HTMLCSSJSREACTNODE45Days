/**
 * Normalize a profile object using **object destructuring in the function parameter list**.
 *
 * Input shape: `{ email, displayName?, role? }`
 * - `role` defaults to `"viewer"` when `undefined` (use a parameter default in the destructuring pattern).
 * - Return `{ primaryEmail, displayName, role }` where `primaryEmail` is `email.trim()`.
 * - `displayName` should be a trimmed string; if missing/`undefined`, use `""` (default in pattern).
 * - If `email` is missing, not a string, or empty after trim, return `null`.
 */
export function normalizeProfile(profile) {
  // TODO(Day22-task03): Implement per TASK_INSTRUCTIONS.md
  return null;
}

/**
 * Parse `"left:right"` strings using **array destructuring** on `split`.
 * - If input is not a string, return `null`.
 * - Missing right side yields empty string for `right`.
 * - Trim both sides.
 */
export function parsePair(pairString) {
  // TODO(Day22-task03): Implement per TASK_INSTRUCTIONS.md
  return null;
}
