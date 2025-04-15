import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from api.serializers import UserSerializer
from django.db.models import Q

from core.models import Room, RoomParticipant, User, Role


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.code_invite = self.scope["url_route"]["kwargs"]["code_invite"]
        self.user = self.scope["user"]
        self.is_in_waiting_state = False

        try:
            self.room = await sync_to_async(Room.objects.get)(
                code_invite=self.code_invite
            )
            self.room_group_name = f"chat_{self.room.id}"
            self.user_group_name = f"user_{self.user.id}"
        except Room.DoesNotExist:
            await self.close()
            return

        # Accept the connection right away
        await self.accept()

        # Always add user to their personal channel
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        print(self.room.id)
        print(self.user.id)
        participant = await sync_to_async(
            lambda: RoomParticipant.objects.filter(
                room=self.room, user=self.user
            ).first()
        )()

        if not participant:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "message": "You are not a participant of this room.",
                    }
                )
            )
            await self.close()
            return

        if self.room.type == "PRIVATE" and not participant.is_approved:
            self.is_in_waiting_state = True
            return

        # User is approved, add them to the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await sync_to_async(
            lambda: RoomParticipant.objects.filter(
                room=self.room, user=self.user
            ).update(is_out=False)
        )()
        user = UserSerializer(self.user).data

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "user_joined", "user": user}
        )

        await self.broadcast_participant_list()
        
        # Broadcast video call participants list to the new user
        await self.broadcast_video_call_participants()

        # If this is an admin and moderator, send them the pending requests list
        if participant.role == Role.MODERATOR or participant.role == Role.ADMIN:
            await self.broadcast_pending_requests()

    async def user_approved(self, event):
        user = event["user"]
        room_id = event["room_id"]
        code_invite = event["code_invite"]

        if user["id"] == self.user.id and self.is_in_waiting_state:
            self.is_in_waiting_state = False

            # Add user to room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            # Notify user about approval
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "user_approved",
                        "user": user,
                        "room_id": room_id,
                        "code_invite": code_invite,
                    }
                )
            )

            # Broadcast user joined to room
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "user_joined", "user": user}
            )

            # Update user list in room
            await self.broadcast_participant_list()
            
            # Broadcast video call participants
            await self.broadcast_video_call_participants()

    async def user_rejected(self, event):
        user = event["user"]
        room_id = event["room_id"]
        code_invite = event["code_invite"]

        if user["id"] == self.user.id and self.is_in_waiting_state:
            self.is_in_waiting_state = False

            # Notify user about rejection
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "user_rejected",
                        "user": user,
                        "room_id": room_id,
                        "code_invite": code_invite,
                    }
                )
            )

    async def user_assigned_moderator(self, event):
        user = event["user"]
        room_id = event["room_id"]
        code_invite = event["code_invite"]

        if user["id"] == self.user.id:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "user_assigned_moderator",
                        "user": user,
                        "room_id": room_id,
                        "code_invite": code_invite,
                    }
                )
            )

            # Update user list in room
            await self.broadcast_pending_requests()
            await self.broadcast_participant_list()

    async def user_revoked_moderator(self, event):
        user = event["user"]
        room_id = event["room_id"]
        code_invite = event["code_invite"]

        if user["id"] == self.user.id:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "user_revoked_moderator",
                        "user": user,
                        "room_id": room_id,
                        "code_invite": code_invite,
                    }
                )
            )

            # Update user list in room
            await self.broadcast_pending_requests()
            await self.broadcast_participant_list()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

        if hasattr(self, "room") and hasattr(self, "user"):
            # Update user status and clear peer ID when disconnecting
            await sync_to_async(
                lambda: RoomParticipant.objects.filter(
                    room=self.room, user=self.user
                ).update(
                    is_out=True, 
                    is_camera_on=False, 
                    is_microphone_on=False,
                    peer_id=None
                )
            )()

            await sync_to_async(
                lambda: User.objects.filter(
                    id=self.user.id).update(is_online=False)
            )()

            user = UserSerializer(self.user).data

            await self.channel_layer.group_send(
                self.room_group_name, {"type": "user_left", "user": user}
            )

            # Broadcast updated participant list and video call participants
            await self.broadcast_participant_list()
            await self.broadcast_video_call_participants()

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get("type")
            
            if message_type == "message":
                user = UserSerializer(self.user).data

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "user": user,
                        "message": text_data_json["message"],
                    },
                )
            elif message_type == "typing":
                user = UserSerializer(self.user).data

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "typing_status",
                        "is_typing": text_data_json["is_typing"],
                        "user": user,
                    },
                )
            # Video call related messages
            elif message_type == "join_video_call":
                peer_id = text_data_json.get("peer_id")
                if peer_id:
                    await self.handle_join_video_call(peer_id)
            elif message_type == "leave_video_call":
                await self.handle_leave_video_call()
            elif message_type == "toggle_camera":
                is_on = text_data_json.get("is_on", False)
                await self.handle_toggle_camera(is_on)
            elif message_type == "toggle_microphone":
                is_on = text_data_json.get("is_on", False)
                await self.handle_toggle_microphone(is_on)
            # PeerJS signaling messages
            elif message_type == "offer":
                await self.handle_offer(text_data_json)
            elif message_type == "answer":
                await self.handle_answer(text_data_json)
            elif message_type == "ice_candidate":
                await self.handle_ice_candidate(text_data_json)
                
        except json.JSONDecodeError:
            print("Invalid JSON received")
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_message",
                    "user": event["user"],
                    "message": event["message"],
                }
            )
        )

    async def typing_status(self, event):
        print(f"Typing status: {event['is_typing']}")
        await self.send(
            text_data=json.dumps(
                {
                    "type": "typing_status",
                    "is_typing": event["is_typing"],
                    "user": event["user"],
                }
            )
        )

    async def user_joined(self, event):
        # Gửi thông tin người dùng khi họ tham gia phòng
        await self.send(
            text_data=json.dumps(
                {"type": "user_joined", "user": event["user"]})
        )

    async def user_left(self, event):
        await self.send(
            text_data=json.dumps({"type": "user_left", "user": event["user"]})
        )

    async def broadcast_participant_list(self):
        participants = await sync_to_async(list)(
            RoomParticipant.objects.filter(room=self.room, is_out=False).select_related(
                "user"
            )
        )

        participant_data_list = []
        for participant in participants:
            user_data = UserSerializer(participant.user).data
            participant_data = {
                "user": user_data,
                "role": participant.role,
                "is_approved": participant.is_approved,
                "is_out": participant.is_out,
            }
            participant_data_list.append(participant_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "update_participant_list",
                "participants": participant_data_list},
        )

    async def update_participant_list(self, event):
        await self.send(
            text_data=json.dumps(
                {"type": "participant_list",
                    "participants": event["participants"]}
            )
        )

    async def broadcast_pending_requests(self):
        try:
            pending_requests = await sync_to_async(list)(
                RoomParticipant.objects.filter(
                    room=self.room, is_approved=False
                ).select_related("user")
            )

            request_list = []
            for participant in pending_requests:
                user_data = UserSerializer(participant.user).data
                participant_data = {
                    "user": user_data,
                    "role": participant.role,
                    "is_approved": participant.is_approved,
                    "is_out": participant.is_out,
                }
                request_list.append(participant_data)

            admin_participants = await sync_to_async(list)(
                RoomParticipant.objects.filter(room=self.room)
                .filter(Q(role=Role.ADMIN) | Q(role=Role.MODERATOR))
                .select_related("user")
            )
            for admin in admin_participants:
                admin_user_group = f"user_{admin.user.id}"
                await self.channel_layer.group_send(
                    admin_user_group,
                    {"type": "update_pending_requests", "requests": request_list},
                )
        except Exception as e:
            print(f"Error in broadcast_pending_requests: {str(e)}")

    async def update_pending_requests(self, event):
        await self.send(
            text_data=json.dumps(
                {"type": "pending_requests", "requests": event["requests"]}
            )
        )

    async def room_ended(self, event):
        """Handle room ended event"""

        await self.send(
            text_data=json.dumps(
                {
                    "type": "room_ended",
                    "room_id": event["room_id"],
                    "code_invite": event["code_invite"],
                }
            )
        )

        # Disconnect user from room
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
    
    # VIDEO CALL METHODS
    
    async def handle_join_video_call(self, peer_id):
        """Handle when a user joins the video call with their peer ID"""
        # Check if we already have 10 people in the call
        active_call_participants = await sync_to_async(
            lambda: RoomParticipant.objects.filter(
                room=self.room, 
                is_out=False,
                peer_id__isnull=False
            ).count()
        )()
        
        # If we already have 10 people in the call, don't allow more
        if active_call_participants >= 10:
            await self.send(
                text_data=json.dumps({
                    "type": "video_call_error",
                    "message": "The video call has reached the maximum capacity of 10 participants."
                })
            )
            return
            
        # Update the participant's peer ID in the database
        await sync_to_async(
            lambda: RoomParticipant.objects.filter(
                room=self.room, user=self.user
            ).update(peer_id=peer_id)
        )()
        
        user = UserSerializer(self.user).data
        
        # Notify everyone that a new user joined the video call
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_joined_video_call",
                "user": user,
                "peer_id": peer_id
            },
        )
        
        # Broadcast updated video call participants
        await self.broadcast_video_call_participants()
    
    async def handle_leave_video_call(self):
        """Handle when a user leaves the video call"""
        # Update the database to clear the peer ID
        await sync_to_async(
            lambda: RoomParticipant.objects.filter(
                room=self.room, user=self.user
            ).update(
                peer_id=None,
                is_camera_on=False,
                is_microphone_on=False
            )
        )()
        
        user = UserSerializer(self.user).data
        
        # Notify everyone that a user left the video call
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_left_video_call",
                "user": user
            },
        )
        
        # Broadcast updated video call participants
        await self.broadcast_video_call_participants()
    
    async def handle_toggle_camera(self, is_on):
        """Handle toggling the camera state"""
        # Update the database with the new camera state
        await sync_to_async(
            lambda: RoomParticipant.objects.filter(
                room=self.room, user=self.user
            ).update(is_camera_on=is_on)
        )()
        
        user = UserSerializer(self.user).data
        
        # Notify everyone about the camera state change
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "camera_toggled",
                "user": user,
                "is_on": is_on
            },
        )
    
    async def handle_toggle_microphone(self, is_on):
        """Handle toggling the microphone state"""
        # Update the database with the new microphone state
        await sync_to_async(
            lambda: RoomParticipant.objects.filter(
                room=self.room, user=self.user
            ).update(is_microphone_on=is_on)
        )()
        
        user = UserSerializer(self.user).data
        
        # Notify everyone about the microphone state change
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "microphone_toggled",
                "user": user,
                "is_on": is_on
            },
        )
    
    async def broadcast_video_call_participants(self):
        """Broadcast the list of active video call participants"""
        participants = await sync_to_async(list)(
            RoomParticipant.objects.filter(
                room=self.room,
                is_out=False,
                peer_id__isnull=False
            ).select_related("user")
        )
        
        video_participants = []
        for participant in participants:
            user_data = UserSerializer(participant.user).data
            participant_data = {
                "user": user_data,
                "peer_id": participant.peer_id,
                "is_camera_on": participant.is_camera_on,
                "is_microphone_on": participant.is_microphone_on
            }
            video_participants.append(participant_data)
        
        # Send to all users in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "update_video_call_participants",
                "participants": video_participants
            },
        )
    
    # PeerJS signaling handlers
    
    async def handle_offer(self, data):
        """Handle WebRTC offer messages (forward to the target peer)"""
        target_peer_id = data.get("target_peer_id")
        offer = data.get("offer")
        sender_peer_id = data.get("sender_peer_id")
        
        if not all([target_peer_id, offer, sender_peer_id]):
            return
        
        # Find the target user based on peer_id
        target_participant = await sync_to_async(
            lambda: RoomParticipant.objects.filter(
                room=self.room,
                peer_id=target_peer_id,
                is_out=False
            ).select_related("user").first()
        )()
        
        if not target_participant:
            return
            
        target_user = target_participant.user
        target_user_group = f"user_{target_user.id}"
        
        # Forward the offer to the target user
        await self.channel_layer.group_send(
            target_user_group,
            {
                "type": "relay_offer",
                "offer": offer,
                "sender_peer_id": sender_peer_id
            }
        )
    
    async def handle_answer(self, data):
        """Handle WebRTC answer messages (forward to the target peer)"""
        target_peer_id = data.get("target_peer_id")
        answer = data.get("answer")
        sender_peer_id = data.get("sender_peer_id")
        
        if not all([target_peer_id, answer, sender_peer_id]):
            return
        
        # Find the target user based on peer_id
        target_participant = await sync_to_async(
            lambda: RoomParticipant.objects.filter(
                room=self.room,
                peer_id=target_peer_id,
                is_out=False
            ).select_related("user").first()
        )()
        
        if not target_participant:
            return
            
        target_user = target_participant.user
        target_user_group = f"user_{target_user.id}"
        
        # Forward the answer to the target user
        await self.channel_layer.group_send(
            target_user_group,
            {
                "type": "relay_answer",
                "answer": answer,
                "sender_peer_id": sender_peer_id
            }
        )
    
    async def handle_ice_candidate(self, data):
        """Handle ICE candidate messages (forward to the target peer)"""
        target_peer_id = data.get("target_peer_id")
        candidate = data.get("candidate")
        sender_peer_id = data.get("sender_peer_id")
        
        if not all([target_peer_id, candidate, sender_peer_id]):
            return
        
        # Find the target user based on peer_id
        target_participant = await sync_to_async(
            lambda: RoomParticipant.objects.filter(
                room=self.room,
                peer_id=target_peer_id,
                is_out=False
            ).select_related("user").first()
        )()
        
        if not target_participant:
            return
            
        target_user = target_participant.user
        target_user_group = f"user_{target_user.id}"
        
        # Forward the ICE candidate to the target user
        await self.channel_layer.group_send(
            target_user_group,
            {
                "type": "relay_ice_candidate",
                "candidate": candidate,
                "sender_peer_id": sender_peer_id
            }
        )
    
    # Event handlers that send to the WebSocket
    
    async def user_joined_video_call(self, event):
        """Send notification when a user joins the video call"""
        await self.send(
            text_data=json.dumps({
                "type": "user_joined_video_call",
                "user": event["user"],
                "peer_id": event["peer_id"]
            })
        )
    
    async def user_left_video_call(self, event):
        """Send notification when a user leaves the video call"""
        await self.send(
            text_data=json.dumps({
                "type": "user_left_video_call",
                "user": event["user"]
            })
        )
    
    async def camera_toggled(self, event):
        """Send notification when a user toggles their camera"""
        await self.send(
            text_data=json.dumps({
                "type": "camera_toggled",
                "user": event["user"],
                "is_on": event["is_on"]
            })
        )
    
    async def microphone_toggled(self, event):
        """Send notification when a user toggles their microphone"""
        await self.send(
            text_data=json.dumps({
                "type": "microphone_toggled",
                "user": event["user"],
                "is_on": event["is_on"]
            })
        )
    
    async def update_video_call_participants(self, event):
        """Send updated list of video call participants"""
        await self.send(
            text_data=json.dumps({
                "type": "video_call_participants",
                "participants": event["participants"]
            })
        )
    
    async def relay_offer(self, event):
        """Relay a WebRTC offer to this client"""
        await self.send(
            text_data=json.dumps({
                "type": "offer",
                "offer": event["offer"],
                "sender_peer_id": event["sender_peer_id"]
            })
        )
    
    async def relay_answer(self, event):
        """Relay a WebRTC answer to this client"""
        await self.send(
            text_data=json.dumps({
                "type": "answer",
                "answer": event["answer"],
                "sender_peer_id": event["sender_peer_id"]
            })
        )
    
    async def relay_ice_candidate(self, event):
        """Relay an ICE candidate to this client"""
        await self.send(
            text_data=json.dumps({
                "type": "ice_candidate",
                "candidate": event["candidate"],
                "sender_peer_id": event["sender_peer_id"]
            })
        )