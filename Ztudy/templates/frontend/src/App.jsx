import { Routes, Route, Navigate } from 'react-router-dom'
import WaitingRoom from './components/WaitingRoom'
import MeetingRoom from './components/MeetingRoom'
import './index.css'

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-semibold text-gray-900">Video Call App</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <Routes>
          <Route path="/" element={<Navigate to="/waiting-room" replace />} />
          <Route path="/waiting-room" element={<WaitingRoom />} />
          <Route path="/meeting" element={<MeetingRoom />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
