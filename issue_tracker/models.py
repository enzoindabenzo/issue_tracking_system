from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50,
                            choices=[('admin', 'Admin'), ('developer', 'Developer'), ('tester', 'Tester')])

    def __str__(self):
        return self.user.username


class Issue(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    issue_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey(User, related_name='created_issues', on_delete=models.CASCADE)
    assigned_to_user = models.ForeignKey(User, related_name='assigned_issues', on_delete=models.SET_NULL, null=True,
                                         blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    issue = models.ForeignKey(Issue, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text[:20]


class Attachment(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    issue = models.ForeignKey(Issue, related_name='attachments', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=200)
    file_url = models.URLField()
    uploaded_by_user = models.ForeignKey(User, related_name='attachments', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name


class UserListReport(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=150)
    email = models.EmailField()
    role = models.CharField(max_length=50)
    registration_date = models.DateTimeField()

    class Meta:
        managed = False  # No migrations will be created for this model


class UserActivityReport(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=150)
    role = models.CharField(max_length=50)
    activities_count = models.IntegerField()
    last_activity_timestamp = models.DateTimeField()

    class Meta:
        managed = False


class IssueSummaryReport(models.Model):
    issue_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    created_by_user_id = models.IntegerField()
    assigned_to_user_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False


class IssueStatusReport(models.Model):
    issue_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    assigned_to_user_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
