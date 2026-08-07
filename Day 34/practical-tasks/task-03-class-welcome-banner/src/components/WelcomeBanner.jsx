import { Component } from 'react'

export default class WelcomeBanner extends Component {
  render() {
    const { title, subtitle } = this.props;
    return (
      <header className="banner">
        <h1>{title}</h1>
        {subtitle && <p>{subtitle}</p>}
      </header>
    )
  }
}
