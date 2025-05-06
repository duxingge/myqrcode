# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model

# # Register your models here.
# User = get_user_model()

# # 解决LogEntry问题
# admin.site.unregister(LogEntry)

# @admin.register(LogEntry)
# class LogEntryAdmin(admin.ModelAdmin):
#     list_display = ['action_time', 'user', 'content_type', 'object_repr']
    
#     def has_add_permission(self, request):
#         return False
    
#     def has_change_permission(self, request, obj=None):
#         return False