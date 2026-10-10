
import { useState } from "react"

export default function Counter() {

  const [count,setCount] = useState(0);

  return (
    
    <section className="counter">
      <output aria-live="polite">{count}</output>
      <div className="row">
        <button type="button" onClick={()=>{setCount(prev=>prev=prev+1)}}>+1</button>
        <button type="button" onClick={()=>{setCount(prev=>prev=prev-1)}}>-1</button>
        <button type="button"onClick={()=>{setCount(prev=>prev=0)}}>Reset</button>
      </div>
    </section>
  )
}
