from django.db import models
from django.contrib.auth.models import User



class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # It basically stores the relationships between to-dos and user. 1 user has a lot of todos.

    def __str__(self): # A way to show the title of the todo's titles in the admin page
        return self.title