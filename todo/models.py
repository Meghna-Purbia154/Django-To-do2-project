from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

# ---------------- Helper for default due date ----------------
def default_due_date():
    return timezone.now().date() + timedelta(days=7)

# ---------------- Profile Model ----------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[('Male','Male'), ('Female','Female')], default='Male')

    def __str__(self):
        return self.user.username

# auto-create Profile when a user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# ---------------- Category Model ----------------
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#c8b3ff")  # pastel color for UI

    class Meta:
        unique_together = (('user', 'name'),)

    def __str__(self):
        return self.name

# ---------------- Task Model ----------------
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    RECUR_CHOICES = [
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=default_due_date)
    recurrence = models.CharField(max_length=10, choices=RECUR_CHOICES, default='none')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_overdue(self):
        return self.status != 'completed' and self.due_date < timezone.localdate()

    def get_absolute_url(self):
        return reverse('task-list')

    def __str__(self):
        return f"{self.title} ({self.user.username})"

# ---------------- SubTask Model ----------------
class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=15, choices=Task.STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.title} - {self.task.title}"

# ---------------- Notification Model ----------------
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message}"
