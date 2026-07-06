/**
 * Bucket HTTP status codes into coarse families using `switch(true)` (or equivalent switch logic).
 *
 * Rules:
 * - `code` must be an integer in [100, 599]; otherwise return `"invalid"`.
 * - 100-199 -> `"informational"`
 * - 200-299 -> `"success"`
 * - 300-399 -> `"redirect"`
 * - 400-499 -> `"client_error"`
 * - 500-599 -> `"server_error"`
 */
export function httpStatusFamily(code) {
  return "invalid";
}
