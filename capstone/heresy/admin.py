from django.contrib import admin

# Register your models here.

from .models  import User, Infantry, Weapons, ArmyLists, ListBlocks
admin.site.register(User)
admin.site.register(Infantry)
admin.site.register(Weapons)
admin.site.register(ArmyLists)
admin.site.register(ListBlocks)
