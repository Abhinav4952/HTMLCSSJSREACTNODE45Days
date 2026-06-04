/**
 * Create a tiny fluent query builder:
 * - `select(fields: string[])` stores fields (non-empty array of non-empty strings) and returns `this`.
 * - `from(table: string)` stores a non-empty trimmed table name and returns `this`.
 * - `build()` returns `SELECT f1, f2 FROM table` based on the last `select`/`from` calls.
 * - If `build()` called before both are set, return empty string.
 */
export function createQueryBuilder() {
  // TODO(Day25-task02): Implement per TASK_INSTRUCTIONS.md
  return {
    select() {
      return this;
    },
    from() {
      return this;
    },
    build() {
      return "INVALID";
    },
  };
}
