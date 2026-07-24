export class StepCounter {
  count = 0;
  step = 1;

  constructor(step = 1) {
    if(Number.isFinite(step) && step>0) this.step=step;
  }

  tick(times = 1) {
    if(Number.isFinite(times) && times>=0) this.count+= this.step*times;
    return this.count;
  }
}
