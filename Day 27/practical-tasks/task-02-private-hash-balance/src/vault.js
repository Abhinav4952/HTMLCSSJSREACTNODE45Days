export class Vault {
  #balance = 0;

  constructor(opening = 0) {
    // TODO(Day27-task02): set #balance to opening if finite number, else 0
  }

  get balance() {
    // TODO(Day27-task02): return #balance
    return Number.NaN;
  }

  deposit(amount) {
    // TODO(Day27-task02): add finite positive amount; return new balance
    return this.#balance;
  }
}
