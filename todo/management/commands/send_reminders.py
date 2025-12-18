from django.core.management.base import BaseCommand
from django.utils import timezone
from todo.models import Task, Notification

class Command(BaseCommand):
    help = 'Send reminders for tasks that have reached their reminder date'

    def handle(self, *args, **options):
        now = timezone.now()
        # Find tasks with reminder_date <= now and not completed
        tasks_to_remind = Task.objects.filter(
            reminder_date__lte=now,
            status__in=['pending', 'in_progress']
        ).exclude(reminder_date__isnull=True)

        reminders_sent = 0
        for task in tasks_to_remind:
            # Check if a reminder notification already exists for this task
            existing_notification = Notification.objects.filter(
                user=task.user,
                task=task,
                message__startswith='Reminder:'
            ).exists()

            if not existing_notification:
                message = f"Reminder: {task.title} is due on {task.due_date}"
                Notification.objects.create(
                    user=task.user,
                    task=task,
                    message=message
                )
                reminders_sent += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Sent reminder for task: {task.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {reminders_sent} reminders')
        )
