/**
 * Return a new array containing `2 * x` for every finite number `x` in `nums` where `x > 0`.
 *
 * Rules:
 * - If `nums` is not an array, return `null`.
 * - Ignore non-numbers and non-finite numbers.
 */
export function doublePositives(nums) {
  if(Array.isArray(nums))
    return nums.filter(x=> typeof x==="number" && Number.isFinite(x) && x>0).map(x=>2*x);
  return null
}
