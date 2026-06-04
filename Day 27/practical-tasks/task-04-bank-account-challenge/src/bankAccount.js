export class BankAccount {
  #balance = 0;
  static count = 0;

  constructor(opening = 0) {
    // TODO(Day27-task04): initialize #balance (finite number else 0); increment static count
  }

  withdraw(amount) {
    // TODO(Day27-task04): finite positive; cannot go below 0; return amount actually withdrawn
    return 0;
  }

  static created() {
    // TODO(Day27-task04): return how many accounts were constructed
    return 0;
  }
}
