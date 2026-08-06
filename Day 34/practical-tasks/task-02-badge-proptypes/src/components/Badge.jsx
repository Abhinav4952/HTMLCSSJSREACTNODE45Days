import PropTypes from 'prop-types'
export default function Badge({label,variant="info",icon=undefined}) {
  
  return (
    <span className={`badge badge--${variant}`}>
    {
      icon && (<span className='badge__icon' aria-hidden>{icon}</span>)
    }
      {label}
    </span>
  )
}

Badge.propTypes = {
  label : PropTypes.string.isRequired,
  icon: PropTypes.string,
  variant: PropTypes.oneOf(["info","warn","success"])
}
