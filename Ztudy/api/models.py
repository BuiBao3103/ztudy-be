from django.db import models
from django_softdelete.models import SoftDeleteModel
from django.contrib.auth.models import AbstractUser, UserManager
from cloudinary.models import CloudinaryField

class SessionGoalsStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    COMPLETED = 'COMPLETED', 'Completed'

class RoomType(models.TextChoices):
    PRIVATE = 'PRIVATE', 'Private'
    PUBLIC = 'PUBLIC', 'Public'

class BackgroundVideoType(SoftDeleteModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BackgroundVideo(models.Model):
    youtube_code = models.CharField(max_length=255, null=False)
    image = CloudinaryField('image', null=True, blank=True)
    type = models.ForeignKey(BackgroundVideoType, on_delete=models.CASCADE, related_name="videos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Video {self.id} - {self.url}"


class SessionGoal(models.Model):
    goal = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=SessionGoalsStatus.choices,
        default=SessionGoalsStatus.OPEN
    )
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="goals")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.goal


class User(SoftDeleteModel, AbstractUser):
    email = models.EmailField(unique=True)
    is_online = models.BooleanField(default=False)
    avatar = CloudinaryField('avatar', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    def __str__(self):
        return self.username


class MotivationalQuote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'"{self.quote}" - {self.author}'

class Sound(models.Model):
    name = models.CharField(max_length=255)
    sound_file = models.FileField(upload_to='sounds/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class RoomCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}_{self.name}"

class Room(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=7, choices=RoomType.choices, default=RoomType.PUBLIC)
    thumbnail = CloudinaryField('thumbnail', null=True, blank=True)
    creator_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms_created', null=True, blank=True)
    code_invite = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(RoomCategory, on_delete=models.SET_NULL, null=True, blank=True)
    max_participants = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class RoomParticipant(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms_joined')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_out = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.room.room_name}'

class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interests")
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, related_name="user_interests")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "category")

    def __str__(self):
        return f"{self.user.id}_{self.user.username} - {self.category.id}_{self.category.name}"


class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='activity_logs')
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    interaction_count = models.IntegerField(default=0)

    def duration(self):
        """Tính tổng thời gian user ở trong phòng (tính theo phút)"""
        if self.left_at:
            return (self.left_at - self.joined_at).total_seconds() / 60
        return 0

    def __str__(self):
        return f"{self.user.username} - {self.room.name}"