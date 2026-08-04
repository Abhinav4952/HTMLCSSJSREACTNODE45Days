/**
 * A reusable “label” renderer that expects `this.brand` and `this.version`.
 * Do not modify this object.
 */
export const labeler = {
  render() {
    return `${this.brand}-${this.version}`;
  },
};

/**
 * Render using `labeler.render` with `host` as the receiver (`this`).
 * Must use `.call`.
 */
export function renderWithHost(host) {
  return labeler.render.call(host);
}

/**
 * Compute max of an array using `Math.max` via `.apply` (not spread).
 */
export function maxWithApply(numbers) {
  return Math.max.apply(null,numbers);
}
