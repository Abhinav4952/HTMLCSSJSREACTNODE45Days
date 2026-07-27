export function hasCaseInsensitiveYes(text) {
  const regex = /yes/i;
  return regex.test(text);
}
