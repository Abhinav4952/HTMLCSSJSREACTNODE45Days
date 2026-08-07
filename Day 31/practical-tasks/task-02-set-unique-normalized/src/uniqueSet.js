export function uniqueSorted(nums) {
  return [...new Set(nums.filter(num=>Number.isFinite(num)).sort())];
}
