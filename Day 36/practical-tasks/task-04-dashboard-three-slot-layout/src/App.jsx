import DashboardLayout from './components/DashboardLayout.jsx'

export default function App() {
  return (
    <DashboardLayout
      leftAside={<div className="panel"><strong>Nav</strong><p>Home</p><p>Reports</p></div>}
      main={
        <div className="panel">
          <h1 style={{ marginTop: 0 }}>Main workspace</h1>
          <p>This column should appear in the center region.</p>
        </div>
      }
      rightAside={<div className="panel"><strong>Widgets</strong><p>Calendar</p><p>Tasks</p></div>}
    />
  )
}
