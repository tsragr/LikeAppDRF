from django.contrib import admin
from account.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'bio', 'created_at', 'updated_at')
    list_filter = ('created_at',)

