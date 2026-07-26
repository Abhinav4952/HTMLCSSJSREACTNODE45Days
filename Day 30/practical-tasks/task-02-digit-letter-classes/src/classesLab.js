export function isThreeDigits(s) {
  const regex = /^\d{3}$/
  return regex.test(s);
}
