/**
 * Return an array of `count` functions such that the `i`th function returns `i` when called.
 * - If `count` is not an integer in `[0, 20]`, return `null`.
 * - Each function must close over the correct index (no shared `var` bug).
 */
export function createIndexHandlers(count) {

  if(Number.isInteger(count) && count>=0 && count<=20) {
    let res = [];

    for(let i = 0;i<count;i++){
      res.push(()=>i);
    }
    return res;
  }

  return null;
}
