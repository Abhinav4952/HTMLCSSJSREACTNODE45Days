export class Rectangle {
  constructor(w, h) {
    this.w = w;
    this.h = h;
  }
  area() {
    if(Number.isFinite(this.w) && this.w>0 && Number.isFinite(this.h) && this.h>0) return this.w*this.h;
    return 0; 
  }
}

export class Square extends Rectangle {
  constructor(side) {
    super(side,side);
  }
}
