from .user_views import UserList, UserRetrieveUpdateDestroy, CheckUserPreferences, AddUserInterest, UploadAvatarView
from .motivational_quote_views import MotivationalQuoteListCreate, MotivationalQuoteRetrieveUpdateDestroy, \
    RandomMotivationalQuoteView
from .google_views import GoogleLogin, GoogleLoginCallback, LoginPage
from .background_video_views import (BackgroundVideoListCreate, BackgroundVideoRetrieveUpdateDestroy,
                                     UploadBackgroundVideoView,
                                     BackgroundVideoTypeListCreate, BackgroundVideoTypeRetrieveUpdateDestroy)
from .session_goal_views import SessionGoalListCreate, SessionGoalRetrieveUpdateDestroy
from .sound_views import SoundList, SoundUpload, SoundDetail
from .room_views import (RoomListCreate, RoomRetrieveUpdateDestroy, UploadThumbnailView,
                         RoomCategoryListCreate, RoomCategoryRetrieveUpdateDestroy,
                         RoomParticipantListCreate, RoomParticipantRetrieveUpdateDestroy,
                         SuggestedRoomsAPIView, JoinRoomAPIView, LeaveRoomAPIView)
from .views import chat_room
