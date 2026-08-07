export function parseJsonSafe(text, fallback = null) {
  try {
    if(typeof text!=="string") return fallback;
    let res = JSON.parse(text)
    return res;
  } catch(err) {
    if(err instanceof SyntaxError) return fallback;
  }
  return null;
}
