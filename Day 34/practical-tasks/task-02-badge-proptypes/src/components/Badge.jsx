import PropTypes from 'prop-types'

// TODO(Day34-task02): Render `label` text inside the span.
// TODO(Day34-task02): Apply correct class names: always include `badge`, plus `badge--${variant}` where variant is one of info|warn|success (default to info when missing).
// TODO(Day34-task02): When `icon` is provided, render it before the label inside a <span className="badge__icon" aria-hidden>.
// TODO(Day34-task02): After the component function, define `Badge.propTypes`: label (string, required), variant (oneOf the three strings), icon (optional string).
export default function Badge() {
  return <span className="badge">Complete Badge TODOs</span>
}
