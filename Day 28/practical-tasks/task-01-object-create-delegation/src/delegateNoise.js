const noiseMethods = {
  label() {
    return this.kind;
  },
};

export function createNoisyThing(kind) {
  const res = Object.create(noiseMethods);
  res.kind = kind;
  return res;
}
