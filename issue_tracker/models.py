from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)  # admin, developer, tester


class Issue(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50)  # open, in progress, resolved, closed
    priority = models.CharField(max_length=50)  # high, medium, low
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_issues', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='assigned_issues', on_delete=models.CASCADE, null=True,
                                    blank=True)


class Comment(models.Model):
    issue = models.ForeignKey(Issue, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Attachment(models.Model):
    issue = models.ForeignKey(Issue, related_name='attachments', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_url = models.URLField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
