/**
 * Bucket HTTP code codes into coarse families using `switch(true)` (or equivalent switch logic).
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
  if(!Number.isInteger(code)) return "invalid"
  switch (true) {
    case code>=100 && code < 200:
      return "informational";

    case code >= 200 && code < 300:
      return "success";

    case code >= 300 && code < 400:
      return "redirect";

    case code >= 400 && code < 500:
      return "client_error";

    case code >= 500 && code < 600:
      return "server_error";
  }
  return "invalid";
}
