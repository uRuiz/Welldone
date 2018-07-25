from django.contrib import admin

# Register your models here.

from articles.models import *

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Favourite)
admin.site.register(Comment)
admin.site.register(Highlight)
admin.site.register(Mentions)
