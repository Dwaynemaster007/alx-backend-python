from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Conversation, Message, User


@admin.register(User)
class ChatUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Profile', {'fields': ('phone_number', 'role')}),)
    list_display = ('username', 'email', 'role', 'is_staff')


admin.site.register(Conversation)
admin.site.register(Message)
