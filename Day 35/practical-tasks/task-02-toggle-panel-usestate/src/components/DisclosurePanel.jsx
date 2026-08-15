import { useState } from "react"
export default function DisclosurePanel({ title, children }) {
  const [isOpen,setIsOpen] = useState(false);
  return (
    <section className="panel">
      <header style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '0.75rem' }}>
        <h2 style={{ margin: 0, fontSize: '1.1rem' }}>{title}</h2>
        <button type="button" onClick={()=>setIsOpen(prev=>!prev)}>{isOpen? "Hide" : "Show"}</button>
      </header>
      {isOpen && 
      <div className="panel__body">
        {children}
      </div>}
    </section>
  )
}
