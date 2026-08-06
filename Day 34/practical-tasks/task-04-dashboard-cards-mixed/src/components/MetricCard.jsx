export default function MetricCard({title,value}) {
  return (
    <article className="metric">
      <h2>{title}</h2>
      <p>{value}</p>
    </article>
  )
}
