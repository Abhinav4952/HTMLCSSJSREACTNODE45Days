/**
 * Return flags for an *own* **data** property descriptor, or `null` if missing/not a data descriptor.
 *
 * Rules:
 * - If `obj` is not an object or is `null`, return `null`.
 * - If the property is not an own property, return `null`.
 * - If the descriptor is an accessor descriptor (`get` or `set` exists), return `null` (this lab is data-only).
 * - Otherwise return `{ writable, enumerable, configurable }` booleans from the descriptor.
 */
export function summarizeOwnDataDescriptor(obj, key) {
  // TODO(Day19-task04): Implement per TASK_INSTRUCTIONS.md
  return null;
}
