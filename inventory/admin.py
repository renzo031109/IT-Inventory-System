from django.contrib import admin
from .models import Item, ItemBase, ItemCode, UOM, Department, Client, Site

class ItemCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'site')


admin.site.site_header = "S360 Inventory System"
admin.site.register(Item)
admin.site.register(ItemBase)
admin.site.register(ItemCode, ItemCodeAdmin)
admin.site.register(UOM)
admin.site.register(Department)
admin.site.register(Client)
admin.site.register(Site)



