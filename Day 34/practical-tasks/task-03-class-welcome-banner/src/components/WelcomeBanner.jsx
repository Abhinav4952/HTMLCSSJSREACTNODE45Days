import { Component } from 'react'

export default class WelcomeBanner extends Component {
  render() {
    // TODO(Day34-task03): Read `title` (string, required for sensible UI) and optional `subtitle` from `this.props`.
    // TODO(Day34-task03): Render a <header className="banner"> containing an <h1> for the title.
    // TODO(Day34-task03): When `subtitle` is present, render it in a <p> under the title. When absent, render no empty <p>.
    return (
      <header className="banner">
        <h1>Welcome banner placeholder</h1>
      </header>
    )
  }
}
