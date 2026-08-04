/**
 * Create a tiny fluent query builder:
 * - `select(fields: string[])` stores fields (non-empty array of non-empty strings) and returns `this`.
 * - `from(table: string)` stores a non-empty trimmed table name and returns `this`.
 * - `build()` returns `SELECT f1, f2 FROM table` based on the last `select`/`from` calls.
 * - If `build()` called before both are set, return empty string.
 */
export function createQueryBuilder() {
  return {
    fields:null,
    table:null,
    select(fields) {
      if(Array.isArray(fields) && fields.length>0 && fields.every(field=> typeof field==="string" && field.trim()!=="")) {
        this.fields=fields.map(field=>field.trim())
      }
      return this;
    },
    from(table) {
      if(typeof table==="string" && table.trim()!=="") this.table=table.trim();
      return this;
    },
    build() {
      if(this.fields===null || this.table===null) return "";
      return `SELECT ${this.fields.join(', ')} FROM ${this.table}`;
    },
  };
}
