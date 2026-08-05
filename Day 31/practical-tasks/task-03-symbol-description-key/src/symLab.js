export function buildSecretBag() {
  const map = new Map()
  return {
    set(kind,value) {
      const key = Symbol.for("kind: " + kind);
      map[key]=value
    },
    get(kind) {
      const key = Symbol.for("kind: " + kind);
      return map[key];
    }
  };
}
