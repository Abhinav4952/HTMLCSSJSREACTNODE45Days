export function countTokens(tokens) {
  let res = new Map();
  for(const token of tokens) {
    if(token.trim()!=="") {
      const key = token.trim().toLowerCase()
      res.set(key,(res.get(key) || 0) + 1);
    }
  }
  return res;
}
