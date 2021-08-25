from django.contrib import admin
from .models import User

class AccountAdmin(admin.ModelAdmin):

    list_display = ['username', 'name', 'is_active', 'is_staff', 'is_superuser']

admin.site.register(User, AccountAdmin)
