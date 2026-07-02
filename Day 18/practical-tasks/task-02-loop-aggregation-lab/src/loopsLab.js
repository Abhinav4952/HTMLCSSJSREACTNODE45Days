/**
 * Sum numbers from left to right, stopping before the running total would exceed `cap`.
 *
 * Rules:
 * - If `cap` is not a finite number, return `0`.
 * - If `nums` is not an array, return `0`.
 * - Treat non-finite numbers and non-numbers in `nums` as **stoppers**: return the sum accumulated **before** that element (do not include the bad element).
 * - If the first element cannot be added without exceeding `cap`, return `0`.
 */
export function sumPrefixUntilCap(nums, cap) {
  if(Number.isFinite(cap) && Array.isArray(nums)) {
    let sum=0;
    for(const i of nums)  {
      if(Number.isNaN(i) || !Number.isFinite(i) || sum+i>cap) {
        return sum;
      }
      sum= sum+i;

    }
    return sum;
  }
  return 0;
}
