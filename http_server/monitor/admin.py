from django.contrib import admin

# Register your models here.
from .models import Storage
class StorageAdmin(admin.ModelAdmin):  # add this
    list_display = ('key', 'value') # add this

admin.site.register(Storage, StorageAdmin)
