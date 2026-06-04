export class StepCounter {
  count = 0;
  step = 1;

  constructor(step = 1) {
    // TODO(Day27-task01): assign this.step if step is a finite number > 0, else keep default 1
  }

  tick(times = 1) {
    // TODO(Day27-task01): increment count by step * times when times is a finite integer >= 0
    return this.count;
  }
}
