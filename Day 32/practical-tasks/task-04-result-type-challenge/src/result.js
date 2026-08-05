export function divide(a, b) {
  try {
    if(b===0) throw new Error("division by zero");
    return {ok : true,value : a/b}
  } catch(err) {
    return {ok : false,error: err.message}
  }
  return { ok: false, error: "TODO" };
}
