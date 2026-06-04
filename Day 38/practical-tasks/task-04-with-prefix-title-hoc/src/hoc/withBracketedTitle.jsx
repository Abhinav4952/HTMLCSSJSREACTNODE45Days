// TODO(Day38-task04): Implement a higher-order component `withBracketedTitle`.
// Requirements:
// - It is a function `withBracketedTitle(Wrapped)` that returns a new component.
// - The returned component renders `<Wrapped {...props} />` but transforms the `title` prop:
//   if `title` is a string, wrap it as `«${title}»`; otherwise pass `title` through unchanged.
// - Forward all other props unchanged.
// - Export **named** export `withBracketedTitle` (already declared below—fill in the implementation).
export function withBracketedTitle(Wrapped) {
  return function BracketedTitle(props) {
    return <Wrapped {...props} />
  }
}
