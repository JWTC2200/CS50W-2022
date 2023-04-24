from django.contrib import admin

# Register your models here.

from .models  import User, Infantry, Weapons
admin.site.register(User)
admin.site.register(Infantry)
admin.site.register(Weapons)
