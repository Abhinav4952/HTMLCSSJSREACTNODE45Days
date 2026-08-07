export function createObjectMetadata() {
  const wm = new WeakMap()
  return {
    tag(obj,label) {
      wm[obj] = label;
    },
    read(obj) {return wm[obj]}
  };
}
