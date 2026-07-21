export class BankAccount {
  #balance = 0;
  static count = 0;

  constructor(opening = 0) {    if(Number.isFinite(opening)) this.#balance=opening;
    BankAccount.count++;
  }

  withdraw(amount) {
    if(Number.isFinite(amount) && amount>0) {
      if(amount>this.#balance) amount= this.#balance
      this.#balance-= amount;  
    } 
    return amount;
  }

  static created() {
    return BankAccount.count;
    return 0;
  }
}
