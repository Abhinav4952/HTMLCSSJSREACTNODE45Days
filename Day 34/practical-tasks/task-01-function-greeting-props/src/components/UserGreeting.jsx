/**
 * Renders a friendly one-line greeting using props.
 */
export default function UserGreeting({name="guest",role = undefined}) {
  return <p>Hello, {name} {role===undefined? "" : `(${role})`}</p>
}
