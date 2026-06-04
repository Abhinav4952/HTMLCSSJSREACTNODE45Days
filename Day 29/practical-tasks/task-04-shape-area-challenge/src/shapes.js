export class Rectangle {
  constructor(w, h) {
    this.w = w;
    this.h = h;
  }
  area() {
    // TODO(Day29-task04): return w*h if finite positives else 0
    return 0;
  }
}

export class Square extends Rectangle {
  constructor(side) {
    // TODO(Day29-task04): super(side, side)
    super(0, 0);
  }
}
