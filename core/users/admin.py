from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	list_display = ('username','email','is_admin', 'is_active')
	list_filter = ('is_admin','is_active')

	fieldsets = (
			(None, {'fields': ('username','email','password')}),
			('Permissions', {'fields': ('is_admin','is_active')}),
			('Personal Data', {'fields': ('city','country', 'birthday')}),
			(None, {'fields': ('image',)}),
		)
	search_fields = ('username','email')
	ordering = ('username','email')

	filter_horizontal = ()



admin.site.unregister(Group)