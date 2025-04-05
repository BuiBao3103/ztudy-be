import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'

function WaitingRoom() {
  const [isMicMuted, setIsMicMuted] = useState(false)
  const [isVideoOff, setIsVideoOff] = useState(false)
  const [username, setUsername] = useState('')
  const videoRef = useRef(null)
  const streamRef = useRef(null)
  const navigate = useNavigate()

  const startVideo = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      })
      streamRef.current = stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream
      }
    } catch (error) {
      console.error('Error accessing media devices:', error)
    }
  }

  useEffect(() => {
    startVideo()

    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop())
      }
    }
  }, [])

  const toggleMic = () => {
    if (streamRef.current) {
      const audioTrack = streamRef.current.getAudioTracks()[0]
      audioTrack.enabled = !audioTrack.enabled
      setIsMicMuted(!isMicMuted)
    }
  }

  const toggleVideo = () => {
    if (streamRef.current) {
      const videoTrack = streamRef.current.getVideoTracks()[0]
      videoTrack.enabled = !videoTrack.enabled
      setIsVideoOff(!isVideoOff)
    }
  }

  const handleJoinMeeting = () => {
    if (!username.trim()) {
      alert('Please enter your name')
      return
    }
    
    // Stop current stream before navigating
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop())
    }

    // Navigate to meeting room with initial states
    navigate('/meeting', {
      state: {
        username,
        initialAudioEnabled: !isMicMuted,
        initialVideoEnabled: !isVideoOff
      }
    })
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-[600px] bg-white rounded-[30px] shadow-xl p-8 border border-gray-100">
        <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">Video & Audio Setup</h2>
        
        <div className="space-y-6">
          {/* Video Preview */}
          <div className="relative w-full aspect-video bg-gray-100 rounded-[20px] overflow-hidden">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className={`w-full h-full object-cover ${isVideoOff ? 'hidden' : ''}`}
            />
            {isVideoOff && (
              <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
                <span className="text-4xl">📷</span>
              </div>
            )}
          </div>

          {/* Controls */}
          <div className="space-y-4">
            <div className="flex gap-4 justify-center">
              <button
                onClick={toggleMic}
                className={`px-6 py-3 rounded-xl font-semibold text-lg transition-all duration-200 ${
                  isMicMuted 
                    ? 'bg-red-500 hover:bg-red-600 text-white' 
                    : 'bg-blue-500 hover:bg-blue-600 text-white'
                }`}
              >
                {isMicMuted ? '🎤 Unmute' : '🎤 Mute'}
              </button>
              <button
                onClick={toggleVideo}
                className={`px-6 py-3 rounded-xl font-semibold text-lg transition-all duration-200 ${
                  isVideoOff 
                    ? 'bg-red-500 hover:bg-red-600 text-white' 
                    : 'bg-blue-500 hover:bg-blue-600 text-white'
                }`}
              >
                {isVideoOff ? '📷 Start Video' : '📷 Stop Video'}
              </button>
            </div>

            <div className="space-y-4">
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your name"
                className="w-full px-6 py-4 bg-gray-50 border border-gray-200 rounded-[20px] focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all text-gray-800 placeholder-gray-400 text-lg"
              />
              <button
                onClick={handleJoinMeeting}
                className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold text-xl py-4 rounded-[20px] transition-colors duration-200 shadow-lg shadow-blue-500/20"
              >
                Join Meeting
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default WaitingRoom 