from django.contrib import admin
from django.db.models import Count, Max, F
from .models import (UserListReport, UserActivityReport, IssueSummaryReport, IssueStatusReport, Issue, Comment,
                     Attachment)
from django.contrib.auth.models import User
from admin_extra_buttons.api import ExtraButtonsMixin, button
from .models import Profile


class UserListReportAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'registration_date')

    @button(label='Generate Report')
    def generate_report(self, request):
        UserListReport.objects.all().delete()  # Clear existing records

        users = User.objects.annotate(
            user_id=F('id'),
            role=F('profile__role'),  # Assuming you have a related profile model
            registration_date=F('date_joined')
        ).values('user_id', 'username', 'email', 'role', 'registration_date')

        UserListReport.objects.bulk_create([UserListReport(**user) for user in users])


class UserActivityReportAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ('user_id', 'username', 'role', 'activities_count', 'last_activity_timestamp')

    @button(label='Generate Report')
    def generate_report(self, request):
        UserActivityReport.objects.all().delete()  # Clear existing records

        users = User.objects.annotate(
            activities_count=Count('created_issues') + Count('comments') + Count('attachments'),
            last_activity_timestamp=Max('created_issues__created_at', 'comments__created_at',
                                        'attachments__uploaded_at')
        ).values('id', 'username', 'profile__role', 'activities_count', 'last_activity_timestamp')

        UserActivityReport.objects.bulk_create([UserActivityReport(
            user_id=user['id'],
            username=user['username'],
            role=user['profile__role'],
            activities_count=user['activities_count'],
            last_activity_timestamp=user['last_activity_timestamp']
        ) for user in users])


class IssueSummaryReportAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = (
        'issue_id', 'title', 'description', 'status', 'priority', 'created_by_user_id', 'assigned_to_user_id',
        'created_at',
        'updated_at')

    @button(label='Generate Report')
    def generate_report(self, request):
        IssueSummaryReport.objects.all().delete()  # Clear existing records

        issues = Issue.objects.all().values(
            'id', 'title', 'description', 'status', 'priority',
            'created_by_id', 'assigned_to_id', 'created_at', 'updated_at'
        )

        IssueSummaryReport.objects.bulk_create([IssueSummaryReport(
            issue_id=issue['id'],
            title=issue['title'],
            description=issue['description'],
            status=issue['status'],
            priority=issue['priority'],
            created_by_user_id=issue['created_by_id'],
            assigned_to_user_id=issue['assigned_to_id'],
            created_at=issue['created_at'],
            updated_at=issue['updated_at']
        ) for issue in issues])


class IssueStatusReportAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = (
        'issue_id', 'title', 'description', 'status', 'priority', 'assigned_to_user_id', 'created_at', 'updated_at')
    list_filter = ('status',)

    @button(label='Generate Report')
    def generate_report(self, request):
        IssueStatusReport.objects.all().delete()  # Clear existing records

        issues = Issue.objects.all().values(
            'id', 'title', 'description', 'status', 'priority',
            'assigned_to_id', 'created_at', 'updated_at'
        )

        IssueStatusReport.objects.bulk_create([IssueStatusReport(
            issue_id=issue['id'],
            title=issue['title'],
            description=issue['description'],
            status=issue['status'],
            priority=issue['priority'],
            assigned_to_user_id=issue['assigned_to_id'],
            created_at=issue['created_at'],
            updated_at=issue['updated_at']
        ) for issue in issues])


admin.site.register(UserListReport, UserListReportAdmin)
admin.site.register(UserActivityReport, UserActivityReportAdmin)
admin.site.register(IssueSummaryReport, IssueSummaryReportAdmin)
admin.site.register(IssueStatusReport, IssueStatusReportAdmin)

admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Attachment)

admin.site.register(Profile)  # Register Profile if defined separately
