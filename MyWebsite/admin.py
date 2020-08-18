from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from MyWebsite.models import EmployeeUser

# Register your models here.

class EmployeeAdmin(UserAdmin):
	list_display = ('email', 'ename', 'last_login', 'is_admin', 'is_staff')
	search_fields = ('email','ename',)
	readonly_fields = ('last_login','employeeid',)

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	ordering = ()

admin.site.register(EmployeeUser, EmployeeAdmin)