export function composeDefaults(base, defaults) {
  return Object.assign(Object.create(base),defaults);
}
