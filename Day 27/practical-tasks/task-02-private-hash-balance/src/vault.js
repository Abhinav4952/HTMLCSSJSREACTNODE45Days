export class Vault {
  #balance = 0;

  constructor(opening = 0) {
    if(Number.isFinite(opening)) this.#balance=opening;
  }

  get balance() {
    return this.#balance;
  }

  deposit(amount) {
    if(Number.isFinite(amount) && amount>0) this.#balance += amount;
    return this.#balance;
  }
}
