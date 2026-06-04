export function Box(value) {
  if (!(this instanceof Box)) {
    return new Box(value);
  }
  this.value = value;
}

export function isBox(x) {
  // TODO(Day28-task03): return boolean instanceof Box
  return false;
}
