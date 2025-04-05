import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import AgoraRTC from 'agora-rtc-sdk-ng';
import { VideoCameraIcon, MicrophoneIcon, XCircleIcon, PhoneXMarkIcon, ComputerDesktopIcon } from '@heroicons/react/24/solid';

// Initialize Agora client
const client = AgoraRTC.createClient({ 
  mode: 'rtc', 
  codec: 'vp8'
});

const MeetingRoom = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { username, initialAudioEnabled, initialVideoEnabled } = location.state || {};

  const [localTracks, setLocalTracks] = useState([]);
  const [remoteUsers, setRemoteUsers] = useState([]);
  const [isVideoEnabled, setIsVideoEnabled] = useState(initialVideoEnabled);
  const [isAudioEnabled, setIsAudioEnabled] = useState(initialAudioEnabled);
  const [isScreenSharing, setIsScreenSharing] = useState(false);
  const [screenTrack, setScreenTrack] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const cleanup = async () => {
    try {
      // Close local tracks
      for (const track of localTracks) {
        track.close();
      }
      setLocalTracks([]);

      // Close screen sharing track
      if (screenTrack) {
        await client.unpublish(screenTrack);
        screenTrack.close();
        setScreenTrack(null);
      }

      // Leave the channel if connected
      if (client.connectionState === 'CONNECTED') {
        await client.leave();
      }

      // Remove all event listeners
      client.removeAllListeners();
      setRemoteUsers([]);
    } catch (err) {
      console.error('Error during cleanup:', err);
    }
  };

  const toggleScreenShare = async () => {
    try {
      if (!isScreenSharing) {
        // Create screen sharing track
        const screenShareTrack = await AgoraRTC.createScreenVideoTrack({
          encoderConfig: {
            width: 1920,
            height: 1080,
            frameRate: 30,
            bitrateMin: 600,
            bitrateMax: 2000,
          }
        });

        // Publish screen track
        await client.publish(screenShareTrack);
        setScreenTrack(screenShareTrack);
        setIsScreenSharing(true);

        // Handle screen share stop
        screenShareTrack.on('track-ended', async () => {
          await client.unpublish(screenShareTrack);
          screenShareTrack.close();
          setScreenTrack(null);
          setIsScreenSharing(false);
        });
      } else if (screenTrack) {
        // Stop screen sharing
        await client.unpublish(screenTrack);
        screenTrack.close();
        setScreenTrack(null);
        setIsScreenSharing(false);
      }
    } catch (error) {
      console.error('Error toggling screen share:', error);
      setError('Failed to toggle screen sharing');
    }
  };

  useEffect(() => {
    // Redirect if no username
    if (!username) {
      navigate('/waiting-room');
      return;
    }

    let mounted = true;

    const init = async () => {
      try {
        await cleanup();
        if (!mounted) return;

        setIsLoading(true);
        setError(null);

        // Get token from backend
        const channelName = import.meta.env.VITE_CHANNEL_NAME || 'test-channel';
        const backendUrl = window.location.hostname === 'localhost' 
          ? 'http://localhost:8000' 
          : import.meta.env.VITE_BACKEND_URL?.trim();

        console.log('Backend URL:', backendUrl);
        const tokenUrl = `${backendUrl}/api/token/?channel=${channelName}`;
        console.log('Fetching token from:', tokenUrl);

        const headers = {
          'Accept': 'application/json'
        };

        if (window.location.hostname !== 'localhost') {
          headers['ngrok-skip-browser-warning'] = 'true';
        }

        const response = await fetch(tokenUrl, {
          method: 'GET',
          headers,
          credentials: 'include'
        });

        console.log('Response:', response);
        

        // Log response details
        console.log('Response status:', response.status);
        console.log('Response headers:', {
          contentType: response.headers.get('content-type'),
          contentLength: response.headers.get('content-length')
        });

        // Clone the response before reading it
        const responseClone = response.clone();
        const responseText = await responseClone.text();
        console.log('Raw response:', responseText); // Log first 200 chars

        if (!response.ok || !response.headers.get('content-type')?.includes('application/json')) {
          throw new Error(`Server returned invalid response: ${response.status} ${response.statusText}`);
        }

        try {
          const data = await response.json();
          console.log('Token response:', { 
            ...data, 
            token: '***', // Hide token in logs
            channel: channelName 
          });

          if (!data.token || !data.app_id) {
            throw new Error('Invalid token response from server');
          }

          if (!mounted) return;

          // Join the channel
          console.log('Joining channel:', {
            appId: data.app_id,
            channel: channelName,
            uid: data.uid
          });

          await client.join(data.app_id, channelName, data.token, data.uid);
          console.log('Successfully joined channel');

          // Setup event handlers
          client.on('user-published', async (user, mediaType) => {
            await client.subscribe(user, mediaType);
            if (mediaType === 'video') {
              setRemoteUsers((prevUsers) => {
                if (prevUsers.every((User) => User.uid !== user.uid)) {
                  return [...prevUsers, user];
                }
                return prevUsers;
              });
            }
            if (mediaType === 'audio') {
              user.audioTrack?.play();
            }
          });

          client.on('user-unpublished', (user, mediaType) => {
            if (mediaType === 'video') {
              setRemoteUsers((prevUsers) => prevUsers.filter((User) => User.uid !== user.uid));
            }
            if (mediaType === 'audio') {
              user.audioTrack?.stop();
            }
          });

          // Create local tracks
          const [audioTrack, videoTrack] = await AgoraRTC.createMicrophoneAndCameraTracks(
            {
              encoderConfig: 'high_quality'
            },
            {
              encoderConfig: {
                width: 640,
                height: 360,
                frameRate: 30,
                bitrateMin: 400,
                bitrateMax: 1000,
              }
            }
          );

          if (!mounted) {
            audioTrack.close();
            videoTrack.close();
            await client.leave();
            return;
          }

          // Set initial states
          if (!initialAudioEnabled) audioTrack.setEnabled(false);
          if (!initialVideoEnabled) videoTrack.setEnabled(false);
          
          setLocalTracks([audioTrack, videoTrack]);
          await client.publish([audioTrack, videoTrack]);
          setIsLoading(false);

        } catch (e) {
          console.error('JSON parse error:', e);
          throw new Error('Server returned invalid JSON response');
        }

      } catch (error) {
        console.error('Error joining channel:', error);
        console.error('Error details:', {
          message: error.message,
          stack: error.stack
        });
        if (mounted) {
          setError(`Failed to join meeting: ${error.message}`);
          setIsLoading(false);
          await cleanup();
        }
      }
    };

    init();

    return () => {
      mounted = false;
      cleanup();
    };
  }, [username, navigate, initialAudioEnabled, initialVideoEnabled]);

  const toggleVideo = async () => {
    if (localTracks[1]) {
      await localTracks[1].setEnabled(!isVideoEnabled);
      setIsVideoEnabled(!isVideoEnabled);
    }
  };

  const toggleAudio = async () => {
    if (localTracks[0]) {
      await localTracks[0].setEnabled(!isAudioEnabled);
      setIsAudioEnabled(!isAudioEnabled);
    }
  };

  const leaveChannel = async () => {
    await cleanup();
    navigate('/waiting-room');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Connecting to meeting...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="bg-red-500/10 p-6 rounded-lg text-center">
          <div className="text-red-500 text-xl mb-4">Failed to join meeting</div>
          <div className="text-gray-300 mb-4">{error}</div>
          <button
            onClick={() => navigate('/waiting-room')}
            className="px-6 py-2 bg-white text-red-500 rounded-lg hover:bg-red-50 transition-colors"
          >
            Return to Waiting Room
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col">
      {/* Main Content Area */}
      <div className="flex-1 flex">
        {/* Main Screen */}
        <div className="flex-1 p-4 flex items-center justify-center">
          <div className="relative w-full max-w-4xl aspect-video bg-gray-800 rounded-lg overflow-hidden">
            {screenTrack ? (
              <div className="w-full h-full" ref={(element) => {
                if (element) {
                  screenTrack.play(element);
                }
              }}></div>
            ) : (
              localTracks[1] && (
                <div className="w-full h-full" ref={(element) => {
                  if (element) {
                    localTracks[1].play(element);
                  }
                }}></div>
              )
            )}
            <div className="absolute bottom-4 left-4 px-3 py-1 bg-black/50 text-white rounded-md">
              {username} {isScreenSharing ? '(Screen)' : '(Camera)'}
            </div>
          </div>
        </div>

        {/* Video Container */}
        <div className="w-64 bg-gray-800 p-2 space-y-2">
          {/* Local Video */}
          <div className="relative aspect-video bg-gray-800 rounded-lg overflow-hidden border-2 border-blue-500">
            {localTracks[1] && !isScreenSharing && (
              <div className="w-full h-full" ref={(element) => {
                if (element) {
                  localTracks[1].play(element);
                }
              }}></div>
            )}
            <div className="absolute bottom-2 left-2 px-2 py-1 bg-black/50 text-white text-sm rounded-md">
              {username} (You)
            </div>
          </div>

          {/* Remote Videos */}
          {remoteUsers.map((user) => (
            <div key={user.uid} className="relative aspect-video bg-gray-800 rounded-lg overflow-hidden border-2 border-pink-500">
              <div className="w-full h-full" ref={(element) => {
                if (element) {
                  user.videoTrack?.play(element);
                }
              }}></div>
              <div className="absolute bottom-2 left-2 px-2 py-1 bg-black/50 text-white text-sm rounded-md">
                User {user.uid}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Controls */}
      <div className="bg-gray-800/90 backdrop-blur-sm p-4">
        <div className="flex justify-center gap-4">
          <button
            onClick={toggleVideo}
            className={`p-4 rounded-full transition-colors ${
              isVideoEnabled 
                ? 'bg-blue-500 hover:bg-blue-600' 
                : 'bg-red-500 hover:bg-red-600'
            }`}
          >
            {isVideoEnabled ? (
              <VideoCameraIcon className="h-6 w-6 text-white" />
            ) : (
              <XCircleIcon className="h-6 w-6 text-white" />
            )}
          </button>

          <button
            onClick={toggleAudio}
            className={`p-4 rounded-full transition-colors ${
              isAudioEnabled 
                ? 'bg-blue-500 hover:bg-blue-600' 
                : 'bg-red-500 hover:bg-red-600'
            }`}
          >
            {isAudioEnabled ? (
              <MicrophoneIcon className="h-6 w-6 text-white" />
            ) : (
              <XCircleIcon className="h-6 w-6 text-white" />
            )}
          </button>

          <button
            onClick={toggleScreenShare}
            className={`p-4 rounded-full transition-colors ${
              isScreenSharing 
                ? 'bg-green-500 hover:bg-green-600' 
                : 'bg-gray-600 hover:bg-gray-700'
            }`}
          >
            <ComputerDesktopIcon className="h-6 w-6 text-white" />
          </button>

          <button
            onClick={leaveChannel}
            className="p-4 rounded-full bg-red-500 hover:bg-red-600 transition-colors"
          >
            <PhoneXMarkIcon className="h-6 w-6 text-white" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default MeetingRoom; 