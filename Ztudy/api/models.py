from django.db import models
from django_softdelete.models import SoftDeleteModel
from django.contrib.auth.models import AbstractUser, UserManager

class SessionGoalsStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    COMPLETED = 'COMPLETED', 'Completed'


class BackgroundVideoType(SoftDeleteModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BackgroundVideo(models.Model):
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


class User(SoftDeleteModel, AbstractUser):
    email = models.EmailField(unique=True)
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

# '1', 'Success is the sum of small efforts, repeated day in and day out.', 'Robert Collier', '2025-02-24 14:23:23.000000', '2025-02-24 14:23:23.000000'
# '2', 'The future belongs to those who believe in the beauty of their dreams.', 'Eleanor Roosevelt', '2025-02-24 14:23:23.000000', '2025-02-24 14:23:23.000000'
# '3', 'Don\'t watch the clock; do what it does. Keep going.', 'Sam Levenson', '2025-02-24 14:23:23.000000', '2025-02-24 14:23:23.000000'
# '4', 'The only way to do great work is to love what you do.', 'Steve Jobs', '2025-02-24 14:23:23.000000', '2025-02-24 14:23:23.000000'
# '5', 'Education is the passport to the future, for tomorrow belongs to those who prepare for it today.', 'Malcolm X', '2025-02-24 14:23:23.000000', '2025-02-24 14:23:23.000000'
# '6', 'Believe you can and you\'re halfway there.', 'Theodore Roosevelt', '2025-02-24 14:23:23.000000', '2025-02-24 14:23:23.000000'
# '7', 'The expert in anything was once a beginner.', 'Helen Hayes', '2025-02-24 14:23:23.000000', '2025-02-24 14:23:23.000000'
# '8', 'Your education is a dress rehearsal for a life that is yours to lead.', 'Nora Ephron', '2025-02-24 14:23:23.000000', '2025-02-24 14:23:23.000000'
# '9', 'It always seems impossible until it’s done.', 'Nelson Mandela', '2025-02-24 14:23:23.000000', '2025-02-24 14:23:23.000000'
# '10', 'Work hard in silence, let your success be the noise.', 'Frank Ocean', '2025-02-24 14:23:23.000000', '2025-02-24 14:23:23.000000'
