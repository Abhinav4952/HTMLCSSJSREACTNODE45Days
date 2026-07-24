export function Box(value) {
  if (!(this instanceof Box)) {
    return new Box(value);
  }
  this.value = value;
}

export function isBox(x) {
  return x instanceof Box;
}
