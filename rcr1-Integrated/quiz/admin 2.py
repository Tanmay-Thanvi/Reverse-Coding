from django.contrib import admin
from .models import question,response,userlist,riddle
# Register your models here.

admin.site.register(question)
admin.site.register(response)
admin.site.register(riddle)
admin.site.register(userlist)