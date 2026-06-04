import { Component } from 'react'

export default class TeamNote extends Component {
  render() {
    // TODO(Day34-task04): Read `author` and `body` from `this.props` and render inside the <article>.
    // Use <h3> for the author name and <p> for the note body text.
    return (
      <article className="note">
        <h3>Author name</h3>
        <p>Note text placeholder</p>
      </article>
    )
  }
}
