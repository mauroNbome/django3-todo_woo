from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin): # This function allows us to see the date of the object, which you can't modify. (we're customizing the admin page)
    readonly_fields = ('created',)

admin.site.register(Todo, TodoAdmin) # Register the model in the admin page