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
export function ledgerBalance(rows) {
  // TODO(Day20-task03): Implement per TASK_INSTRUCTIONS.md
  return null;
}
