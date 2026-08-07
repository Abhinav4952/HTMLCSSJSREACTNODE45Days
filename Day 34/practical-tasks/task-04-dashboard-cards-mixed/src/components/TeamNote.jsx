import { Component } from 'react'

export default class TeamNote extends Component {
  render() {
    const {author,body} = this.props;
    return (
      <article className="note">
        <h3>{author}</h3>
        <p>{body}</p>
      </article>
    )
  }
}
