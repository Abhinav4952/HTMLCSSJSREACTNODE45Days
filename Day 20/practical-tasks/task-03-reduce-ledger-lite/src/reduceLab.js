/**
 * Sum signed ledger rows.
 *
 * Each row is `{ kind: "credit" | "debit", amount: number }`.
 *
 * Rules:
 * - If `rows` is not an array, return `null`.
 * - Credits add `amount`, debits subtract `amount`.
 * - Ignore rows that are not plain objects with valid `kind` and finite positive `amount`.
 */

function isPlainObject(x){
  if(x===null) return false;
  let p= Object.getPrototypeOf(x)
  return p===Object.prototype || p===null;
}

export function ledgerBalance(rows) {
  if(Array.isArray(rows)) {
  return rows.filter(row => isPlainObject(row) && (row.kind === "credit" || row.kind === "debit") && Number.isFinite(row.amount) && row.amount > 0).reduce((sum, row) => sum + (row.kind === "credit" ? row.amount : -row.amount),0);
}
  return null;
}
