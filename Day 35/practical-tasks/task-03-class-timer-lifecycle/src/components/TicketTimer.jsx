import { Component } from 'react'

export default class TicketTimer extends Component {
  constructor(props) {
    super(props)
    this.state = { seconds: 0 }
    this._intervalId = null
  }

  componentDidMount() {
    this._intervalId = window.setInterval(this.tick.bind(this), 1000)
  }

  componentWillUnmount() {
    if (this._intervalId !== null) {
      window.clearInterval(this._intervalId)
      this._intervalId = null
    }
  }

  tick() {
    this.setState((prev) => ({
      seconds: prev.seconds + 1,
    }))
  }

  render() {
    return <p className="timer">Elapsed: {this.state.seconds}s</p>
  }
}