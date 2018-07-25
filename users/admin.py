from django.contrib import admin

# Register your models here.
from users.models import *

admin.site.register(Follower)
admin.site.register(Email)
admin.site.register(Profile)
