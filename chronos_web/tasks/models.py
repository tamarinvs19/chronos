from django.db import models
from django.utils.translation import gettext_lazy as _

from datetime import datetime


class Task(models.Model):
    class TaskStatus(models.TextChoices):
        TODO = "TODO", _("To do")
        INPROGRESS = "IN_PROGRESS", _("In progress")
        DONE = "DONE", _("Done")
        CANCELLED = "CANCELLED", _("Cancelled")

    title = models.CharField(max_length=300)
    description = models.TextField(default="", blank=True)
    status = models.CharField(
        max_length=11,
        choices=TaskStatus.choices,
        default=TaskStatus.TODO,
    )
    creation_datetime = models.DateTimeField(default=datetime.now, blank=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    finish_datetime = models.DateTimeField(blank=True, null=True)

    dependencies = models.ManyToManyField("Task", related_name="continuations", blank=True)

    def __str__(self):
        return f"Task({self.title})"


# class Queue(models.Model):
#     capacity = models.IntegerField(default=1)
#     queue = models.ForeignKey("Queue", on_delete=models.CASCADE, null=True, related_name="tasks")
#
#     def __str__(self):
#         return f"Queue({self.capacity})"

