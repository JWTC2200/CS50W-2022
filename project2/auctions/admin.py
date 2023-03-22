from django.contrib import admin

from .models import User, Listings, Bids, Comments, Watchlist

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("item_name", "seller", "status", "winner")
    
class WatchAdmin(admin.ModelAdmin):
    list_display = ("user", "watched_item")


admin.site.register(User)
admin.site.register(Listings, ListingAdmin)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist, WatchAdmin)