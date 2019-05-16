from django.contrib import admin
from bysj import models
# Register your models here.

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['url', 'title', 'is_menu', 'icon']
    list_editable = ['title', 'is_menu', 'icon']

admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.Role)
admin.site.register(models.UserInfo)


