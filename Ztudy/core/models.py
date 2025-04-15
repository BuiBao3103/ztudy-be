from django.utils import timezone
from django.db import models
from django_softdelete.models import SoftDeleteModel
from django.contrib.auth.models import AbstractUser, UserManager
from cloudinary.models import CloudinaryField

from core.utils import decode_emoji


class SessionGoalsStatus(models.TextChoices):
    OPEN = "OPEN", "Open"
    COMPLETED = "COMPLETED", "Completed"


class RoomType(models.TextChoices):
    PRIVATE = "PRIVATE", "Private"
    PUBLIC = "PUBLIC", "Public"


class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    USER = "USER", "User"
    MODERATOR = "MODERATOR", "Moderator"


class MonthlyLevel(models.TextChoices):
    MEMBER = "MEMBER", "Member (0-10m)"
    ENTRY = "ENTRY", "Entry (10m-60m)"
    BEGINNER = "BEGINNER", "Beginner (1-3h)"
    INTERMEDIATE = "INTERMEDIATE", "Intermediate (3-6h)"
    PROFICIENT = "PROFICIENT", "Proficient (6-10h)"
    ADVANCED = "ADVANCED", "Advanced (10-20h)"
    EXPERT = "EXPERT", "Expert (20-40h)"
    A_PLUS_STUDENT = "A_PLUS_STUDENT", "A+ Student (40-60h)"
    MASTER = "MASTER", "Master (60-80h)"
    GRANDMASTER = "GRANDMASTER", "Grandmaster (80-140h)"
    STUDY_MACHINE = "STUDY_MACHINE", "Study-Machine (140-200h)"
    STUDY_MASTER = "STUDY_MASTER", "Study Master (200+h)"

    @classmethod
    def get_role_from_time(cls, monthly_study_time):
        """
        Hàm tính cấp độ dựa trên thời gian học (giờ).
        """
        if monthly_study_time < 10 / 60:
            return cls.MEMBER
        elif monthly_study_time < 1:
            return cls.ENTRY
        elif monthly_study_time < 3:
            return cls.BEGINNER
        elif monthly_study_time < 6:
            return cls.INTERMEDIATE
        elif monthly_study_time < 10:
            return cls.PROFICIENT
        elif monthly_study_time < 20:
            return cls.ADVANCED
        elif monthly_study_time < 40:
            return cls.EXPERT
        elif monthly_study_time < 60:
            return cls.A_PLUS_STUDENT
        elif monthly_study_time < 80:
            return cls.MASTER
        elif monthly_study_time < 140:
            return cls.GRANDMASTER
        elif monthly_study_time < 200:
            return cls.STUDY_MACHINE
        else:
            return cls.STUDY_MASTER

    @classmethod
    def compare_levels(cls, level1, level2):
        level_ranks = [
            cls.MEMBER,
            cls.ENTRY,
            cls.BEGINNER,
            cls.INTERMEDIATE,
            cls.PROFICIENT,
            cls.ADVANCED,
            cls.EXPERT,
            cls.A_PLUS_STUDENT,
            cls.MASTER,
            cls.GRANDMASTER,
            cls.STUDY_MACHINE,
            cls.STUDY_MASTER,
        ]
        rank1 = level_ranks.index(level1)
        rank2 = level_ranks.index(level2)
        return rank1 - rank2

    @classmethod
    def next_level(cls, level):
        level_ranks = [
            cls.MEMBER,
            cls.ENTRY,
            cls.BEGINNER,
            cls.INTERMEDIATE,
            cls.PROFICIENT,
            cls.ADVANCED,
            cls.EXPERT,
            cls.A_PLUS_STUDENT,
            cls.MASTER,
            cls.GRANDMASTER,
            cls.STUDY_MACHINE,
            cls.STUDY_MASTER,
        ]
        current_index = level_ranks.index(level)
        if current_index < len(level_ranks) - 1:
            return level_ranks[current_index + 1]
        return None

    @classmethod
    def time_to_next_level(cls, level, monthly_study_time):
        if level == cls.MEMBER:
            return 10 / 60 - monthly_study_time
        elif level == cls.ENTRY:
            return 1 - monthly_study_time
        elif level == cls.BEGINNER:
            return 3 - monthly_study_time
        elif level == cls.INTERMEDIATE:
            return 6 - monthly_study_time
        elif level == cls.PROFICIENT:
            return 10 - monthly_study_time
        elif level == cls.ADVANCED:
            return 20 - monthly_study_time
        elif level == cls.EXPERT:
            return 40 - monthly_study_time
        elif level == cls.A_PLUS_STUDENT:
            return 60 - monthly_study_time
        elif level == cls.MASTER:
            return 80 - monthly_study_time
        elif level == cls.GRANDMASTER:
            return 140 - monthly_study_time
        elif level == cls.STUDY_MACHINE:
            return 200 - monthly_study_time
        elif level == cls.STUDY_MASTER:
            return 0
        return 0

    @classmethod
    def progress(cls, level, monthly_study_time):
        if level == cls.MEMBER:
            return monthly_study_time / (10 / 60)
        elif level == cls.ENTRY:
            return monthly_study_time / 1
        elif level == cls.BEGINNER:
            return monthly_study_time / 3
        elif level == cls.INTERMEDIATE:
            return monthly_study_time / 6
        elif level == cls.PROFICIENT:
            return monthly_study_time / 10
        elif level == cls.ADVANCED:
            return monthly_study_time / 20
        elif level == cls.EXPERT:
            return monthly_study_time / 40
        elif level == cls.A_PLUS_STUDENT:
            return monthly_study_time / 60
        elif level == cls.MASTER:
            return monthly_study_time / 80
        elif level == cls.GRANDMASTER:
            return monthly_study_time / 140
        elif level == cls.STUDY_MACHINE:
            return monthly_study_time / 200
        elif level == cls.STUDY_MASTER:
            return 1
        return 0


class BackgroundVideoType(SoftDeleteModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return decode_emoji(self.name)


class BackgroundVideo(models.Model):
    youtube_url = models.URLField()

    image = CloudinaryField("image", null=True, blank=True)
    type = models.ForeignKey(
        BackgroundVideoType, on_delete=models.CASCADE, related_name="videos"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Video {self.id} - {self.youtube_url} - {self.type.name}"


class SessionGoal(models.Model):
    goal = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=SessionGoalsStatus.choices,
        default=SessionGoalsStatus.OPEN,
    )

    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="goals")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.goal} - {self.status}"


class User(SoftDeleteModel, AbstractUser):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)
    is_online = models.BooleanField(default=False)
    avatar = CloudinaryField("avatar", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    monthly_study_time = models.FloatField(default=0)
    monthly_level = models.CharField(
        max_length=20, choices=MonthlyLevel.choices, default=MonthlyLevel.MEMBER
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email


class UserFavoriteVideo(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite_videos')
    youtube_url = models.URLField(unique=True)
    image = models.URLField(max_length=500, null=True, blank=True) 
    name = models.CharField(max_length=255, default="")
    author_name = models.CharField(max_length=255, default="", blank=True)
    author_url = models.URLField(max_length=500, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.youtube_url}"


class MotivationalQuote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quote} - {self.author}"


class Sound(models.Model):
    name = models.CharField(max_length=255)
    sound_file = models.FileField(upload_to="sounds/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RoomCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = CloudinaryField("thumbnail", null=True, blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=7, choices=RoomType.choices, default=RoomType.PUBLIC
    )
    thumbnail = CloudinaryField("thumbnail", null=True, blank=True)
    creator_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rooms_created",
        null=True,
        blank=True,
    )
    code_invite = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(
        RoomCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    max_participants = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class RoomParticipant(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="participants"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rooms_joined"
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.USER)
    is_out = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} in {self.room.name}"


class Interest(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="interests")
    category = models.ForeignKey(
        RoomCategory, on_delete=models.CASCADE, related_name="user_interests"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "category")

    def __str__(self):
        return f"{self.user.email} - {self.category.name}"


class UserActivityLog(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activity_logs"
    )
    room = models.ForeignKey(
        "Room", on_delete=models.CASCADE, related_name="activity_logs"
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    interaction_count = models.IntegerField(default=0)

    def duration(self):
        if self.left_at:
            return (self.left_at - self.joined_at).total_seconds() / 3600
        return 0

    def __str__(self):
        return f"{self.user.email} - {self.room.name}"


class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    total_time = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.email} - {self.date} - {self.total_time} hours"
