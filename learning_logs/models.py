from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Topic(models.Model):
    """笔记的主题"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    topic_text = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "主题"
        verbose_name_plural = "主题"

    def __str__(self):
        return self.topic_text


class Entry(models.Model):
    """条目"""
    entry_text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="entries")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "条目"
        verbose_name_plural = "条目"

    def __str__(self):
        return self.entry_text[:50]
