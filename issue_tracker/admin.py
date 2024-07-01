from django.contrib import admin
from .models import User, Issue, Comment, Attachment

admin.site.register(User)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Attachment)
