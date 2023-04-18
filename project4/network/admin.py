from django.contrib import admin

from .models import User, Posts, Follows


admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Follows)

# Register your models here.
