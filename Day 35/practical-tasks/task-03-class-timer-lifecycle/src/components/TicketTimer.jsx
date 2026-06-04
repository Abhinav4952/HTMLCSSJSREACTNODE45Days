import { Component } from 'react'

export default class TicketTimer extends Component {
  constructor(props) {
    super(props)
    this.state = { seconds: 0 }
    this._intervalId = null
  }

  // TODO(Day35-task03): In `componentDidMount`, start `window.setInterval` every 1000ms that calls `this.tick`.
  // Store the interval id on `this._intervalId`.
  componentDidMount() {
    // mount hook intentionally empty until you implement the TODO above
  }

  // TODO(Day35-task03): In `componentWillUnmount`, clear the interval using `window.clearInterval` if `this._intervalId` is set.
  componentWillUnmount() {
    // unmount hook intentionally empty until you implement the TODO above
  }

  tick() {
    // TODO(Day35-task03): Increment `seconds` using the functional `setState` form: `this.setState((prev) => ({ seconds: prev.seconds + 1 }))`.
  }

  render() {
    return <p className="timer">Elapsed: {this.state.seconds}s</p>
  }
}
