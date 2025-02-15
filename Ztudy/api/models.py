from django.db import models
from softdelete.models import SoftDeleteModel


class SessionGoalsStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    COMPLETED = 'COMPLETED', 'Completed'


class BackgroundVideoType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BackgroundVideo(SoftDeleteModel):
    url = models.URLField(max_length=255)
    image = models.URLField(max_length=255, null=True, blank=True)
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


class User(SoftDeleteModel):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    hash_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class MotivationalQuote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'"{self.quote}" - {self.author}'
