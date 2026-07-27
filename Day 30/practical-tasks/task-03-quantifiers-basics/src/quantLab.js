export function splitCommaList(s) {
  return s.split(/\s*,\s*/).filter(str=> str!=="");
}
