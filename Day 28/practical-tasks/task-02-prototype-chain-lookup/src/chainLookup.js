export function readInherited(obj, key) {
  let p = obj;

  while(p!==null){
    if(Object.hasOwn(p,key)) return p[key];
    p = Object.getPrototypeOf(p);
  }
  return undefined;
}
