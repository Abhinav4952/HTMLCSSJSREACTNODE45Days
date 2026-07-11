/**
 * Return `port` unless it is `null` or `undefined`, otherwise return `3000`.
 * Must use **nullish coalescing** (`??`), not `||`.
 */
export function defaultPort(port) {
  
  return port??3000;
}

/**
 * Return `title` unless it is `null` or `undefined`, otherwise `"Untitled"`.
 * Empty string is a valid title and must be preserved.
 */
export function defaultTitle(title) {
  return title??"Untitled";
}
