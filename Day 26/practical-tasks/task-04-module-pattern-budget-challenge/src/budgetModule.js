/**
 * Module-style budget API with **private** balance (closure).
 *
 * Return `{ deposit, withdraw, balance }` where:
 * - `balance()` returns current balance.
 * - `deposit(amount)` adds finite positive `amount`; ignore invalid amounts; return new balance.
 * - `withdraw(amount)` subtracts finite positive `amount` **without** letting balance go negative;
 *   return amount actually withdrawn (may be less than requested if insufficient funds).
 */
export function createBudget(startingBalance = 0) {
  let curr=startingBalance;

  return {
    balance() {
      return curr;
    },
    deposit(amount) {
      if(Number.isFinite(amount) && amount>0) curr+=amount;
      return curr;
    },
    withdraw(amount) {
      if(Number.isFinite(amount) && amount>0 && amount<curr) curr-=amount;
      else if(amount>curr) {
        amount = curr;
        curr=0;
      }
      return amount;
    }
  }
  return null;
}
