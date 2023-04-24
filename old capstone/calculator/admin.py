from django.contrib import admin

# Register your models here.

from .models  import User, Artifact, Artifact_Set, Characters

admin.site.register(User)
admin.site.register(Artifact)
admin.site.register(Artifact_Set)
admin.site.register(Characters)